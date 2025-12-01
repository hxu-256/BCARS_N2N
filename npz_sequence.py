# npz_sequence.py
import numpy as np
from tensorflow.keras.utils import Sequence

class NPZMultiShardSequence(Sequence):
    def __init__(self, npz_paths, batch_size=8, shuffle=True, seed=42):
        self.files = [np.load(p, mmap_mode='r') for p in npz_paths]
        self.axes = str(self.files[0]["axes"])
        s1 = self.files[0]["X"].shape
        for f in self.files[1:]:
            assert str(f["axes"]) == self.axes, "axes mismatch"
            assert f["X"].shape[1:] == s1[1:], "patch shape mismatch"
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.rng = np.random.default_rng(seed)
        # build global index of (shard, local_idx)
        self.index = np.array([(sid, i)
                               for sid, f in enumerate(self.files)
                               for i in range(f["X"].shape[0])],
                               dtype=np.int64)
        self.on_epoch_end()

    def __len__(self):
        return (len(self.index) + self.batch_size - 1) // self.batch_size

    def __getitem__(self, i):
        sl = slice(i*self.batch_size, (i+1)*self.batch_size)
        pairs = self.index[sl]
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
        return Xb, Yb

    def on_epoch_end(self):
        if self.shuffle:
            self.rng.shuffle(self.index)
