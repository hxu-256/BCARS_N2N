# make_single_dataset_simulated.py
import os, glob
import numpy as np
from utils.datagen import create_spend_patches

# ---------- Config ----------
DATA_FOLDER = "./data_simulated/processed"     # output of generate_bcars.py
OUT_DIR     = "./data_simulated/"
os.makedirs(OUT_DIR, exist_ok=True)

# Which simulated field to train on.
# Options: 'Z_noisy', 'noisy_bcars', 'bcars_noise_free'
DATA_KEY = "Z_noisy"

DATASET_PATH = os.path.join(OUT_DIR, f"training_sim_{DATA_KEY}_20260513.npz")

PATCH_SIZE = (32, 32, 96)
STRIDE     = (16, 16, 48)

# Optional spatial cropping (matches the slow/fast axis logic in your H5 pipeline).
# Set all to 0 / None to disable.
SLOW_AXIS_START = 0
FAST_AXIS_START = 0
FAST_AXIS_SIZE  = None   # None -> use everything after FAST_AXIS_START


def npz_to_patches(npz_path, data_key, patch_size, stride,
                   slow_axis_start=0, fast_axis_start=0, fast_axis_size=None):
    """Load a simulated BCARS NPZ and produce SPEND training patches.

    Simulated arrays are stored as (ny, nx, n_wn) and are already wavenumber-cropped
    by generate_bcars.py, so we skip the wn-mask step from the H5 pipeline.
    """
    with np.load(npz_path) as f:
        if data_key not in f.files:
            raise KeyError(
                f"Key '{data_key}' not in {os.path.basename(npz_path)}. "
                f"Available: {f.files}"
            )
        arr = f[data_key].astype(np.float32)  # (ny, nx, n_wn)

    # Optional spatial cropping (analogous to your H5 slow/fast-axis trim)
    if slow_axis_start or fast_axis_start or fast_axis_size:
        arr = arr[slow_axis_start:, :, :]
        if fast_axis_size is None:
            fast_axis_size = arr.shape[0]
        fast_axis_end = fast_axis_start + fast_axis_size
        arr = arr[:, fast_axis_start:fast_axis_end, :]

    X, Y = create_spend_patches(
        raw=arr,
        permute_axis=2,     # (y,x,w) axis
        patch_size=patch_size,
        stride=stride,
        flip=True,
        rotate=True,
    )

    # (S, Y, X, Z) -> (S, Z, Y, X) -> add channel -> (S, C, Z, Y, X)
    Xz = X.transpose(0, 3, 1, 2)[:, None, ...]
    Yz = Y.transpose(0, 3, 1, 2)[:, None, ...]
    return Xz, Yz


if __name__ == "__main__":
    npzs = sorted(glob.glob(os.path.join(DATA_FOLDER, "*.npz")))
    if not npzs:
        raise FileNotFoundError(f"No NPZ files found in {DATA_FOLDER}")

    print(f"Using key: '{DATA_KEY}'  ({len(npzs)} file(s))")

    all_X, all_Y = [], []
    for i, p in enumerate(npzs, 1):
        Xz, Yz = npz_to_patches(
            p,
            data_key        = DATA_KEY,
            patch_size      = PATCH_SIZE,
            stride          = STRIDE,
            slow_axis_start = SLOW_AXIS_START,
            fast_axis_start = FAST_AXIS_START,
            fast_axis_size  = FAST_AXIS_SIZE,
        )
        all_X.append(Xz)
        all_Y.append(Yz)
        print(f"[{i}/{len(npzs)}] collected {Xz.shape[0]} samples from "
              f"{os.path.basename(p)}  (mean={Xz.mean():+.3e}, std={Xz.std():.3e})")

    X = np.concatenate(all_X, axis=0)
    Y = np.concatenate(all_Y, axis=0)

    rng  = np.random.default_rng(15)
    perm = rng.permutation(X.shape[0])
    X    = X[perm]
    Y    = Y[perm]

    axes = "SCZYX"
    print(f"\nIn-memory dataset: X:{X.shape} Y:{Y.shape} axes:{axes} "
          f"(~{(X.nbytes + Y.nbytes)/1e9:.2f} GB)")

    np.savez(DATASET_PATH, X=X, Y=Y, axes=axes, source_key=DATA_KEY)
    print(f"Saved: {DATASET_PATH}")