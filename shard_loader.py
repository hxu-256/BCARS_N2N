# shard_loader.py
import numpy as np
from tensorflow.keras.utils import Sequence
from csbdeep.utils import (
    axes_check_and_normalize, axes_dict, move_channel_for_backend, backend_channels_last
)

class NPZShardSequenceBackendAware(Sequence):
    """
    Shard streaming for CSBDeep with correct channel placement per backend.
    Expects each shard to contain X, Y, axes with identical shapes except S (samples).
    """
    def __init__(self, npz_paths, batch_size=4, shuffle=True, seed=42):
        assert len(npz_paths) > 0, "No shards provided."
        self.files = [np.load(p, mmap_mode='r') for p in npz_paths]
        self.axes_orig = axes_check_and_normalize(str(self.files[0]["axes"]))
        # sanity checks
        shape_ref = self.files[0]["X"].shape
        for f in self.files[1:]:
            assert axes_check_and_normalize(str(f["axes"])) == self.axes_orig, "axes mismatch across shards"
            assert f["X"].shape[1:] == shape_ref[1:], "patch shape mismatch across shards"

        self.batch_size = int(batch_size)
        self.shuffle = bool(shuffle)
        self.rng = np.random.default_rng(seed)

        # build global index of (shard_id, local_idx)
        self.index = np.array([(sid, i)
                               for sid, f in enumerate(self.files)
                               for i in range(f["X"].shape[0])],
                               dtype=np.int64)
        self.on_epoch_end()

        # derive final axes string after channel move (match csbdeep.load_training_data behavior)
        ax = axes_dict(self.axes_orig)
        # remove C, then reinsert depending on backend
        axes_wo_c = self.axes_orig.replace('C','')
        if backend_channels_last():
            self.axes_final = axes_wo_c + 'C'
        else:
            self.axes_final = axes_wo_c[:1] + 'C' + axes_wo_c[1:]

    def __len__(self):
        return (len(self.index) + self.batch_size - 1) // self.batch_size

    def __getitem__(self, i):
        sl = slice(i*self.batch_size, (i+1)*self.batch_size)
        pairs = self.index[sl]

        # group by shard to minimize tiny random reads
        by_shard = {}
        for sid, li in pairs:
            by_shard.setdefault(int(sid), []).append(int(li))

        Xb_list, Yb_list = [], []
        for sid, lis in by_shard.items():
            f = self.files[sid]
            lis = np.asarray(lis, dtype=np.int64)
            Xb_list.append(f["X"][lis])
            Yb_list.append(f["Y"][lis])

        Xb = np.concatenate(Xb_list, axis=0)
        Yb = np.concatenate(Yb_list, axis=0)

        # move channel to match backend (exactly like load_training_data)
        channel = axes_dict(self.axes_orig)['C']
        Xb = move_channel_for_backend(Xb, channel=channel)
        Yb = move_channel_for_backend(Yb, channel=channel)
        return Xb, Yb

    def on_epoch_end(self):
        if self.shuffle:
            self.rng.shuffle(self.index)


def load_training_data_sharded(
    files,                    # list/tuple of .npz shard paths
    validation_split=0.1,
    axes=None,               # optional override; otherwise read from first shard
    n_images=None,           # optional cap on total images across all shards
    shuffle=True,
    seed=42,
    as_generators=True,      # True -> return Sequences; False -> concatenate to arrays
    batch_size=4,
    verbose=False
):
    """
    Shard-aware version of csbdeep.io.load_training_data.

    Returns:
      if as_generators:
        (train_seq, val_seq), None, axes_final
      else:
        (X_train, Y_train), (X_val, Y_val), axes_final
    """
    assert 0 <= float(validation_split) < 1
    files = list(files)
    assert len(files) > 0, "No shard files given."

    # inspect first shard
    f0 = np.load(files[0], mmap_mode='r')
    axes0 = axes_check_and_normalize(str(f0["axes"]) if axes is None else axes)
    C = axes_dict(axes0)['C']

    # count total samples
    counts = []
    shapes_ok = True
    shape1 = f0["X"].shape[1:]
    for p in files:
        d = np.load(p, mmap_mode='r')
        counts.append(d["X"].shape[0])
        shapes_ok &= (axes_check_and_normalize(str(d["axes"])) == axes0 and d["X"].shape[1:] == shape1)
    assert shapes_ok, "All shards must share same axes and non-sample dims."

    total = sum(counts)
    if n_images is None:
        n_images = total
    n_images = min(n_images, total)
    n_val = max(1, int(round(n_images * validation_split))) if validation_split > 0 else 0
    n_train = n_images - n_val if validation_split > 0 else n_images
    assert n_train > 0 and (n_val >= 0)

    # Build a global index list (shard, local_idx) truncated to n_images
    gidx = []
    for sid, p in enumerate(files):
        s = counts[sid]
        gidx.extend([(sid, i) for i in range(s)])
        if len(gidx) >= n_images:
            gidx = gidx[:n_images]
            break
    gidx = np.asarray(gidx, dtype=np.int64)

    rng = np.random.default_rng(seed)
    if shuffle:
        rng.shuffle(gidx)

    if as_generators:
        # split shards lists for train/val by mapping pairs to their shard sets
        gidx_train = gidx[:n_train]
        gidx_val   = gidx[n_train:] if n_val > 0 else np.empty((0,2), dtype=np.int64)

        # choose shard files participating in each split
        shard_ids_train = sorted(set(int(sid) for sid, _ in gidx_train))
        shard_ids_val   = sorted(set(int(sid) for sid, _ in gidx_val))

        train_files = [files[i] for i in shard_ids_train]
        val_files   = [files[i] for i in shard_ids_val] if n_val > 0 else []

        train_seq = NPZShardSequenceBackendAware(train_files, batch_size=batch_size, shuffle=True, seed=seed)
        val_seq   = NPZShardSequenceBackendAware(val_files,   batch_size=batch_size, shuffle=False, seed=seed+1) if n_val>0 else None

        # derive final axes string (same logic as Sequence)
        axes_wo_c = axes0.replace('C','')
        axes_final = axes_wo_c + 'C' if backend_channels_last() else axes_wo_c[:1] + 'C' + axes_wo_c[1:]

        if verbose:
            print(f"[sharded] total images considered: {n_images} (train {n_train}, val {n_val})")
            print(f"[sharded] axes (final): {axes_final}")
            print(f"[sharded] train shards: {len(train_files)}, val shards: {len(val_files)}")

        return (train_seq, val_seq), None, axes_final

    else:
        # Concatenate into arrays (uses RAM). We respect backend channel move like original.
        # Pre-allocate by reading first sample shape
        sample = np.load(files[0], mmap_mode='r')["X"][0:1]
        X_list, Y_list = [], []
        taken = 0
        for p in files:
            d = np.load(p, mmap_mode='r')
            remaining = n_images - taken
            if remaining <= 0: break
            take = min(remaining, d["X"].shape[0])
            X_list.append(d["X"][:take])
            Y_list.append(d["Y"][:take])
            taken += take
        X = np.concatenate(X_list, axis=0)
        Y = np.concatenate(Y_list, axis=0)

        # split train/val
        X_t, Y_t = None, None
        if n_val > 0:
            X_t, Y_t = X[-n_val:], Y[-n_val:]
            X,   Y   = X[:n_train], Y[:n_train]

        # move channels
        channel = axes_dict(axes0)['C']
        if X_t is not None:
            X_t = move_channel_for_backend(X_t, channel=channel)
            Y_t = move_channel_for_backend(Y_t, channel=channel)
        X = move_channel_for_backend(X, channel=channel)
        Y = move_channel_for_backend(Y, channel=channel)

        # build final axes string
        axes_wo_c = axes0.replace('C','')
        axes_final = axes_wo_c + 'C' if backend_channels_last() else axes_wo_c[:1] + 'C' + axes_wo_c[1:]

        if verbose:
            ax = axes_dict(axes_final)
            n_dim = sum(a in 'TZYX' for a in axes_final)
            n_channel_in, n_channel_out = X.shape[ax['C']], Y.shape[ax['C']]
            image_size = tuple(X.shape[ax[a]] for a in axes_final if a in 'TZYX')
            print('number of training images:\t', len(X))
            print('number of validation images:\t', len(X_t) if X_t is not None else 0)
            print('image size (%dD):\t\t' % n_dim, image_size)
            print('axes:\t\t\t\t', axes_final)
            print('channels in / out:\t\t', n_channel_in, '/', n_channel_out)

        data_val = (X_t, Y_t) if n_val > 0 else None
        return (X, Y), data_val, axes_final
