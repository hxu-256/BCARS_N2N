# BCARS Noise2Noise (N2N)

Self-supervised Noise2Noise denoising of broadband CARS (BCARS) hyperspectral cubes, as used
in *Denoising broadband CARS hyperspectral images on variance-stabilized data: a unified
benchmark* ([journal], [year]).

Built on **[CSBDeep / CARE](https://github.com/CSBDeep/CSBDeep)** (Weigert et al., *Nat.
Methods* 2018, MPI-CBG Dresden): the 3-D U-Net, training loop and `CARE` model API come from
CSBDeep. This repository adds the BCARS data generation, the odd/even spectral split, and the
training and inference entry points. The Noise2Noise principle is Lehtinen et al., *ICML*
2018; the odd/even spectral-channel construction for hyperspectral coherent Raman follows the
SPEND application of N2N.

## Idea

The intrinsic spectral resolution (6–7 cm⁻¹) is several times the camera sampling (~2 cm⁻¹), so
adjacent spectral channels carry a redundant signal with independent noise. Splitting the
variance-stabilized (VST) cube into odd and even channels gives two noisy views of the same
scene, and a network trained to map one onto the other converges to the noise-free signal — no
ground truth and no clean corpus needed.

## Contents

```
datagen.py                    simulated cubes (generate_bcars.py .npz) -> training patches .npz
utils/datagen.py              odd/even split, patch extraction, augmentation (create_spend_patches)
training_demo.ipynb           trains the model used for the paper's simulated results
testing_demo_simulated.ipynb  applies it to the held-out simulated cubes -> n2n_restored_*.npz
```

## Workflow

**1. Patches.** Put the simulated cubes from `generate_bcars.py` in `data_simulated/processed/`
and run `python datagen.py`. It reads `Z_noisy` (the VST cube) from each `.npz`, splits odd/even
along the spectral axis, extracts 32×32×96 patches with stride 16×16×48 (flips and rotations
on), shuffles with a fixed seed, and writes `data_simulated/training_sim_Z_noisy_<date>.npz`
holding `X`, `Y` and `axes="SCZYX"`. `DATA_KEY` also accepts `noisy_bcars` or
`bcars_noise_free` for control experiments.

**2. Training** (`training_demo.ipynb`). CARE `Config`: 3-D U-Net, depth 4, 32 base filters,
3×3×3 kernels, residual output, one input and one output channel, 100 epochs × 100 steps,
10% validation split. Training then continues for three further rounds of 100 epochs with the
learning rate stepped down by hand (CSBDeep default 4·10⁻⁴ → 2·10⁻⁴ → 1·10⁻⁴), so the model
sees ~400 epochs in total. The model is written to `models/<name>/`.

**3. Inference** (`testing_demo_simulated.ipynb`). Loads a model by name, predicts each
held-out cube, and saves `n2n_restored_<cube>.npz` with the `restored` array next to the input.

## Model weights

**The trained weights are not available.** They were lost with the training container, and
`models/` is untracked. The configuration above is enough to retrain, but retrained weights
will not reproduce the paper's N2N numbers exactly. The denoised cubes the paper reports are
deposited at [Zenodo DOI].

## Scope

This repository covers the **simulated** N2N results. The experimental cubes (glycerol, bead,
*C. elegans*) were denoised with a separate model trained outside this repository; its outputs
are in the Zenodo deposit and its settings are in the paper's supplementary material.

## Environment

Python 3.11, TensorFlow 2.x, `csbdeep`, `numpy`, `matplotlib`, `tifffile`. A GPU is strongly
recommended for training; inference on one cube takes minutes.

## Related

- Processing pipeline (VST, detrending, CCV, phase retrieval) and the paper's metrics:
  [pipeline repo URL]
- Data and per-method results: [Zenodo DOI]

## Citation

Please cite the paper above, along with CSBDeep/CARE (Weigert et al. 2018) and Noise2Noise
(Lehtinen et al. 2018).
