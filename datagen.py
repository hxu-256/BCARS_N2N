# make_shards.py -> make_single_dataset.py (in-memory aggregation)
import os, glob, h5py, numpy as np
from lazy5.inspect import get_attrs_dset
from utils.datagen import create_spend_patches

DATA_FOLDER = "./data/preprocessed"
OUT_DIR = "./data"
os.makedirs(OUT_DIR, exist_ok=True)
DATASET_PATH = os.path.join(OUT_DIR, "patches_all.npz")

def h5_to_patches(h5_path, patch_size=(32,32,96), stride=(16,16,48)):
    with h5py.File(h5_path, 'r') as f:
        raw_ratio = f['preprocessed_images/medfilter_ratio']  # adjust if needed

        # ----- wavenumber selection -----
        attrs = get_attrs_dset(f, 'preprocessed_images/medfilter_ratio')
        coeffs = attrs['Calib.a_vec']
        n_pix  = 2304
        ctr    = attrs['Calib.ctr_wl0']
        probe  = attrs['Calib.probe'] * 1e-7
        converted_nm = np.polyval(coeffs, np.arange(n_pix)) * 1e-7
        wn = 1/converted_nm - 1/probe

        slow_axis_start = 24
        fast_axis_start = 140
        ratio = raw_ratio[slow_axis_start:,:,:]
        fast_axis_end = fast_axis_start + ratio.shape[0]
        wn_mask = (wn >= 400) & (wn <= 1800)
        indices = np.where(wn_mask)[0]
        ratio_selected = ratio[:, fast_axis_start:fast_axis_end, indices]

        # ----- patching pipeline -----
        X, Y = create_spend_patches(
            raw=ratio_selected,
            permute_axis=0,               # (y,x,w) axis
            patch_size=patch_size,
            stride=stride,
            flip=True,
            rotate=True
        )

        # (S, Y, X, Z) -> (S, Z, Y, X) -> add channel -> (S, C, Z, Y, X)
        Xz = X.transpose(0,3,1,2)[:,None,...]
        Yz = Y.transpose(0,3,1,2)[:,None,...]
        return Xz, Yz  # keep in RAM

if __name__ == "__main__":
    h5s = sorted(glob.glob(os.path.join(DATA_FOLDER, "*.h5")))
    all_X, all_Y = [], []

    for i, h5 in enumerate(h5s, 1):
        Xz, Yz = h5_to_patches(h5)
        all_X.append(Xz)
        all_Y.append(Yz)
        print(f"[{i}/{len(h5s)}] collected {Xz.shape[0]} samples from {os.path.basename(h5)}")

    # Concatenate everything into one big array in RAM
    X = np.concatenate(all_X, axis=0)
    Y = np.concatenate(all_Y, axis=0)

    # Global shuffle
    rng = np.random.default_rng(15)
    perm = rng.permutation(X.shape[0])
    X = X[perm]
    Y = Y[perm]

    axes = "SCZYX"
    bytes_total = X.nbytes + Y.nbytes
    print(f"In-memory dataset: X:{X.shape} Y:{Y.shape} axes:{axes} (~{bytes_total/1e9:.2f} GB)")

    # Optional: save a single compressed file
    np.savez_compressed(DATASET_PATH, X=X, Y=Y, axes=axes)
    print(f"Saved single dataset: {DATASET_PATH}")