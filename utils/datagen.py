"""
SPEND preprocessing utilities for hyperspectral BCARS/SRS data.

Pipeline: raw (x, y, ω) -> odd/even permutation along least-correlated axis ->
paired stacks for N2N -> (optional) patching + augmentations -> dataset.

This module is framework-agnostic (NumPy), with an optional PyTorch Dataset.

Author: you
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator, Optional, Sequence, Tuple, List, Callable
import numpy as np

try:
    import torch
    from torch.utils.data import Dataset
    _TORCH_AVAILABLE = True
except ImportError:
    _TORCH_AVAILABLE = False

try:
    from tqdm import tqdm
    _TQDM_AVAILABLE = True
except ImportError:
    _TQDM_AVAILABLE = False
    def tqdm(iterable, **kwargs):
        return iterable

try:
    import psutil
    _PSUTIL_AVAILABLE = True
except ImportError:
    _PSUTIL_AVAILABLE = False
except Exception:
    _TORCH_AVAILABLE = False
    Dataset = object  # type: ignore

AxisLike = int | str
Array = np.ndarray


# ------------------------------
# Helpers
# ------------------------------

def _axis_to_int(axis: AxisLike) -> int:
    if isinstance(axis, int):
        if axis in (0, 1, 2):
            return axis
        raise ValueError("axis int must be 0, 1, or 2 for (x, y, w)")
    axis = axis.lower()
    mapping = {"x": 0, "y": 1, "w": 2, "omega": 2, "ω": 2, "spectral": 2}
    if axis not in mapping:
        raise ValueError(f"Unknown axis string: {axis}")
    return mapping[axis]


def _maybe_pad_to_even(a: Array, axis: int, mode: str = "drop") -> Tuple[Array, Optional[int]]:
    """Ensure length along axis is even.

    mode="drop": drop the last slice if odd (recommended; unbiased)
    mode="reflect": reflect-pad one slice at end (keeps length)

    Returns (array, dropped_index_or_None)
    """
    n = a.shape[axis]
    if n % 2 == 0:
        return a, None
    if mode == "drop":
        # drop the last index along axis
        idx = [slice(None)] * a.ndim
        idx[axis] = slice(0, n - 1)
        return a[tuple(idx)], n - 1
    if mode == "reflect":
        pad_before = [(0, 0)] * a.ndim
        pad_before[axis] = (0, 1)
        return np.pad(a, pad_before, mode="reflect"), None
    raise ValueError("mode must be 'drop' or 'reflect'")


def _odd_even_concat(a: Array, axis: int) -> Tuple[Array, Array]:
    """Split a into odd/even index slices along axis and concatenate.

    Returns (odd_first, even_first), both with same shape as input.
    """
    sel = [slice(None)] * a.ndim

    sel_odd = sel.copy(); sel_odd[axis] = slice(1, None, 2)
    sel_even = sel.copy(); sel_even[axis] = slice(0, None, 2)

    odd = a[tuple(sel_odd)]
    even = a[tuple(sel_even)]

    # Interleave by concatenation along axis: odd+even vs even+odd
    odd_first = np.concatenate([odd, even], axis=axis)
    even_first = np.concatenate([even, odd], axis=axis)

    return odd_first, even_first


def _window_slices(shape: Tuple[int, int, int],
                   patch: Tuple[int, int, int],
                   stride: Tuple[int, int, int]) -> Iterator[Tuple[slice, slice, slice]]:
    """Generate 3D slice windows for given shape, patch, and stride."""
    sx, sy, sw = shape
    px, py, pw = patch
    dx, dy, dw = stride

    xmax = max(1, (sx - px) // dx + 1)
    ymax = max(1, (sy - py) // dy + 1)
    wmax = max(1, (sw - pw) // dw + 1)

    for ix in range(xmax):
        xs = ix * dx
        xe = xs + px
        if xe > sx:  # tail coverage
            xs = sx - px
            xe = sx
        for iy in range(ymax):
            ys = iy * dy
            ye = ys + py
            if ye > sy:
                ys = sy - py
                ye = sy
            for iw in range(wmax):
                ws = iw * dw
                we = ws + pw
                if we > sw:
                    ws = sw - pw
                    we = sw
                yield slice(xs, xe), slice(ys, ye), slice(ws, we)


# ------------------------------
# Normalization and Filtering
# ------------------------------

def _memory_check(n_required_memory_bytes: int, thresh_free_frac: float = 0.5) -> None:
    """Check if enough memory is available."""
    try:
        if _PSUTIL_AVAILABLE:
            mem = psutil.virtual_memory()
            mem_frac = n_required_memory_bytes / mem.available
            if mem_frac > thresh_free_frac:
                print(f'Warning: will use {n_required_memory_bytes/1024**2:.0f} MB '
                      f'({100*mem_frac:.1f}%) of available memory.')
            if mem_frac > 1:
                raise MemoryError('Not enough available memory.')
        else:
            if n_required_memory_bytes > 1024**3:  # 1GB
                print(f'Warning: will use {n_required_memory_bytes/1024**2:.0f} MB of memory.')
    except Exception:
        pass  # Silently continue if memory check fails


def norm_percentiles(percentiles: Tuple[float, float] = (1.0, 99.8), relu_last: bool = False) -> Callable:
    """Normalize patches based on percentiles.
    
    Parameters
    ----------
    percentiles : tuple
        (pmin, pmax) percentile values for normalization
    relu_last : bool
        If True, clips minimum to 0 (for ReLU output layers)
        
    Returns
    -------
    callable
        Normalization function that takes (patches_x, patches_y) and returns normalized versions
    """
    pmin, pmax = percentiles
    
    def _normalize(patches_x: Array, patches_y: Array) -> Tuple[Array, Array]:
        def _normalize_single(patches):
            # Compute percentiles across all patches
            p_low = np.percentile(patches, pmin)
            p_high = np.percentile(patches, pmax)
            # Normalize to [0, 1] range
            patches_norm = (patches - p_low) / (p_high - p_low + 1e-8)
            return np.clip(patches_norm, 0, 1)
        
        patches_x_norm = _normalize_single(patches_x)
        if relu_last:
            # For ReLU output, keep minimum at 0
            patches_y_norm = _normalize_single(patches_y)
        else:
            patches_y_norm = _normalize_single(patches_y)
        
        return patches_x_norm, patches_y_norm
    
    return _normalize


def signal_patch_filter(threshold: float = 0.1, percentile: float = 95.0) -> Callable:
    """Filter out patches with low signal content.
    
    Parameters
    ---------- 
    threshold : float
        Fraction of max signal below which patches are filtered out
    percentile : float
        Percentile to use for signal strength estimation
        
    Returns
    -------
    callable
        Filter function that takes (patches_x, patches_y) and returns filtered versions
    """
    def _filter(patches_x: Array, patches_y: Array) -> Tuple[Array, Array]:
        # Compute signal strength for each patch
        signal_strength = np.array([
            np.percentile(patch, percentile) for patch in patches_x
        ])
        
        # Keep patches above threshold
        if len(signal_strength) > 0:
            thresh_val = threshold * np.percentile(signal_strength, 90)
            mask = signal_strength > thresh_val
            
            if not np.any(mask):
                # If no patches pass, keep the top 10%
                n_keep = max(1, len(patches_x) // 10)
                top_indices = np.argsort(signal_strength)[-n_keep:]
                mask = np.zeros(len(patches_x), dtype=bool)
                mask[top_indices] = True
        else:
            mask = np.ones(len(patches_x), dtype=bool)
        
        return patches_x[mask], patches_y[mask]
    
    return _filter


# ------------------------------
# Core class
# ------------------------------

@dataclass
class SPENDPreprocessor:
    """SPEND permutation + patching pipeline (NumPy).

    Parameters
    ----------
    permute_axis: axis along which to permute ("x", "y", "w" or 0/1/2)
    pad_mode: how to handle odd length along permute axis: "drop" or "reflect"
    patch_size: 3D patch size in (px, py, pw); if None, no patching
    stride: 3D stride in (sx, sy, sw); if None and patch_size set, defaults to patch_size (non-overlap)
    rotate: enable 90° rotations in x–y during augmentation
    flip: enable random horizontal/vertical flips in x–y during augmentation
    seed: RNG seed for deterministic augmentations (optional)
    """
    permute_axis: AxisLike = "w"
    pad_mode: str = "drop"
    patch_size: Optional[Tuple[int, int, int]] = None
    stride: Optional[Tuple[int, int, int]] = None
    rotate: bool = True
    flip: bool = True
    seed: Optional[int] = None

    def _rng(self) -> np.random.Generator:
        return np.random.default_rng(self.seed)

    # ---- permutation ----
    def permute(self, a: Array) -> Tuple[Array, Array]:
        """Return (input_stack, target_stack) via odd/even concatenations."""
        if a.ndim != 3:
            raise ValueError("Input array must be 3D (x, y, w)")
        axis = _axis_to_int(self.permute_axis)
        a2, _ = _maybe_pad_to_even(a, axis=axis, mode=self.pad_mode)
        inp, tgt = _odd_even_concat(a2, axis=axis)
        return inp, tgt

    # ---- patching ----
    def _extract_patches_pair(self, inp: Array, tgt: Array) -> Tuple[Array, Array]:
        if self.patch_size is None:
            return inp[None, ...], tgt[None, ...]
        stride = self.stride if self.stride is not None else self.patch_size
        patches_inp: List[Array] = []
        patches_tgt: List[Array] = []
        for xs, ys, ws in _window_slices(inp.shape, self.patch_size, stride):
            patches_inp.append(inp[xs, ys, ws])
            patches_tgt.append(tgt[xs, ys, ws])
        return np.stack(patches_inp, 0), np.stack(patches_tgt, 0)

    # ---- augmentations ----
    def _augment_xy(self, x: Array) -> Array:
        """Random rotations/flips in x–y. Expects shape (..., w) with x as dim0, y as dim1."""
        rng = self._rng()
        out = x
        if self.rotate:
            k = int(rng.integers(0, 4))  # 0,1,2,3 -> 0°,90°,180°,270°
            if k:
                out = np.rot90(out, k=k, axes=(0, 1))
        if self.flip:
            if rng.random() < 0.5:
                out = np.flip(out, axis=0)
            if rng.random() < 0.5:
                out = np.flip(out, axis=1)
        return out

    def _augment_xy_pair(self, x: Array, y: Array) -> Tuple[Array, Array]:
        """Apply same random augmentation to both x and y"""
        rng = self._rng()
        # Generate random parameters once
        k = int(rng.integers(0, 4))  # rotation
        flip_h = rng.random() < 0.5
        flip_v = rng.random() < 0.5
        
        # Apply same transforms to both
        if self.rotate and k > 0:
            x = np.rot90(x, k=k, axes=(0, 1))
            y = np.rot90(y, k=k, axes=(0, 1))
        if self.flip and flip_h:
            x = np.flip(x, axis=0)
            y = np.flip(y, axis=0)
        if self.flip and flip_v:
            x = np.flip(x, axis=1)
            y = np.flip(y, axis=1)
        return x, y

    # ---- end-to-end ----
    def run(self, a: Array, return_patches: bool = True) -> Tuple[Array, Array]:
        """Full preprocessing: permute -> (optional) patch -> (optional) augment.

        Returns
        -------
        (X, Y): arrays of shape (N, px, py, pw) if patching enabled, else (1, x, y, w)
        """
        inp, tgt = self.permute(a)
        X, Y = self._extract_patches_pair(inp, tgt)
        
        # Apply stochastic augmentation per patch PAIR (FIXED)
        if self.rotate or self.flip:
            X_aug = []
            Y_aug = []
            for x_patch, y_patch in zip(X, Y):
                x_aug, y_aug = self._augment_xy_pair(x_patch, y_patch)
                X_aug.append(x_aug)
                Y_aug.append(y_aug)
            X = np.stack(X_aug, 0)
            Y = np.stack(Y_aug, 0)
        
        # Apply normalization if specified
        if hasattr(self, 'normalization') and self.normalization is not None:
            X, Y = self.normalization(X, Y)
        
        # Apply patch filtering if specified  
        if hasattr(self, 'patch_filter') and self.patch_filter is not None:
            X, Y = self.patch_filter(X, Y)
        
        return X, Y


# ------------------------------
# Optional: PyTorch dataset for online sampling
# ------------------------------

class SPENDDataset(Dataset):
    """Online patch-sampling Dataset for PyTorch.

    Uses SPENDPreprocessor.permute() once, then samples patches on-the-fly
    with random spatial crops and augmentations.

    Example
    -------
    pp = SPENDPreprocessor(permute_axis="w", pad_mode="drop", rotate=True, flip=True)
    inp, tgt = pp.permute(raw)  # raw: (x, y, w)
    ds = SPENDDataset(inp, tgt, patch_size=(64,64,16), steps_per_epoch=1024, seed=0)
    loader = torch.utils.data.DataLoader(ds, batch_size=8, shuffle=False)
    """
    def __init__(self,
                 inp: Array,
                 tgt: Array,
                 patch_size: Tuple[int, int, int] = (64, 64, 16),
                 steps_per_epoch: int = 1024,
                 seed: Optional[int] = None,
                 to_channels_first: bool = True,
                 normalization: Optional[Callable] = None):
        if not _TORCH_AVAILABLE:
            raise ImportError("PyTorch not available. Install torch to use SPENDDataset.")
        assert inp.shape == tgt.shape and inp.ndim == 3, "inp/tgt must be same shape (x,y,w)"
        self.inp = inp
        self.tgt = tgt
        self.patch = patch_size
        self.steps = steps_per_epoch
        self.rng = np.random.default_rng(seed)
        self.to_ch_first = to_channels_first
        self.normalization = normalization

    def __len__(self) -> int:
        return self.steps

    def _rand_crop_slices(self) -> Tuple[slice, slice, slice]:
        sx, sy, sw = self.inp.shape
        px, py, pw = self.patch
        x0 = 0 if sx == px else int(self.rng.integers(0, sx - px + 1))
        y0 = 0 if sy == py else int(self.rng.integers(0, sy - py + 1))
        w0 = 0 if sw == pw else int(self.rng.integers(0, sw - pw + 1))
        return slice(x0, x0 + px), slice(y0, y0 + py), slice(w0, w0 + pw)

    def _augment_xy(self, a: Array) -> Array:
        # mirror of SPENDPreprocessor logic
        k = int(self.rng.integers(0, 4))
        if k:
            a = np.rot90(a, k=k, axes=(0, 1))
        if self.rng.random() < 0.5:
            a = np.flip(a, axis=0)
        if self.rng.random() < 0.5:
            a = np.flip(a, axis=1)
        return a

    def _augment_xy_pair(self, x: Array, y: Array) -> Tuple[Array, Array]:
        """Apply same random augmentation to both x and y"""
        # Generate random parameters once
        k = int(self.rng.integers(0, 4))  # rotation
        flip_h = self.rng.random() < 0.5
        flip_v = self.rng.random() < 0.5
        
        # Apply same transforms to both
        if k > 0:
            x = np.rot90(x, k=k, axes=(0, 1))
            y = np.rot90(y, k=k, axes=(0, 1))
        if flip_h:
            x = np.flip(x, axis=0)
            y = np.flip(y, axis=0)
        if flip_v:
            x = np.flip(x, axis=1)
            y = np.flip(y, axis=1)
        return x, y

    def __getitem__(self, idx: int):  # type: ignore[override]
        xs, ys, ws = self._rand_crop_slices()
        x = self.inp[xs, ys, ws]
        y = self.tgt[xs, ys, ws]
        
        # Apply SAME augmentation to both patches (FIXED)
        x, y = self._augment_xy_pair(x, y)
        
        # Apply normalization if specified
        if self.normalization is not None:
            x_norm, y_norm = self.normalization(x[None, ...], y[None, ...])
            x, y = x_norm[0], y_norm[0]
        
        # Convert to torch tensors, channels-first as (C, H, W) with C=pw
        if self.to_ch_first:
            x = np.moveaxis(x, -1, 0)
            y = np.moveaxis(y, -1, 0)
        x_t = torch.from_numpy(x.copy()).float()
        y_t = torch.from_numpy(y.copy()).float()
        return x_t, y_t


# ------------------------------
# Convenience API
# ------------------------------

def preprocess_spend(
    raw: Array,
    permute_axis: AxisLike = "w",
    pad_mode: str = "drop",
    patch_size: Optional[Tuple[int, int, int]] = (64, 64, 16),
    stride: Optional[Tuple[int, int, int]] = None,
    rotate: bool = True,
    flip: bool = True,
    seed: Optional[int] = None,
) -> Tuple[Array, Array]:
    """One-shot SPEND preprocessing returning paired patches for N2N.

    Returns X, Y of shape (N, px, py, pw).
    """
    pp = SPENDPreprocessor(
        permute_axis=permute_axis,
        pad_mode=pad_mode,
        patch_size=patch_size,
        stride=stride,
        rotate=rotate,
        flip=flip,
        seed=seed,
    )
    return pp.run(raw, return_patches=True)


# ------------------------------
# Enhanced API with Normalization and Filtering
# ------------------------------

def create_spend_patches(
    raw: Array,
    permute_axis: AxisLike = "w",
    pad_mode: str = "drop",
    patch_size: Tuple[int, int, int] = (64, 64, 16),
    stride: Optional[Tuple[int, int, int]] = None,
    rotate: bool = True,
    flip: bool = True,
    seed: Optional[int] = None,
    normalization: Optional[Callable] = norm_percentiles(),
    patch_filter: Optional[Callable] = None,
    verbose: bool = True,
) -> Tuple[Array, Array]:
    """Create normalized training patches for N2N with all CSBDeep features.
    
    Parameters
    ----------
    raw : Array
        Raw hyperspectral data (x, y, w)
    permute_axis : AxisLike
        Axis along which to permute ("x", "y", "w" or 0/1/2)
    pad_mode : str
        How to handle odd length: "drop" or "reflect"
    patch_size : Tuple[int, int, int]
        3D patch size (px, py, pw)
    stride : Optional[Tuple[int, int, int]]
        3D stride; if None, defaults to patch_size (non-overlapping)
    rotate : bool
        Enable 90° rotations during augmentation
    flip : bool
        Enable random flips during augmentation
    seed : Optional[int]
        Random seed for reproducible augmentations
    normalization : Optional[Callable]
        Normalization function (default: percentile normalization)
    patch_filter : Optional[Callable]
        Function to filter out low-signal patches
    verbose : bool
        Print progress and statistics
        
    Returns
    -------
    Tuple[Array, Array]
        (X, Y) normalized patch arrays of shape (N, px, py, pw)
    """
    if verbose:
        print('='*50)
        print(f'SPEND Preprocessing Pipeline')
        print(f'Raw data shape: {raw.shape}')
        print(f'Patch size: {patch_size}')
        print(f'Permutation axis: {permute_axis}')
        print(f'Normalization: {"Yes" if normalization else "No"}')
        print(f'Patch filter: {"Yes" if patch_filter else "No"}')
        print('='*50)
    
    # Memory check
    if stride is None:
        stride = patch_size
    n_patches_estimate = np.prod([
        max(1, (s - p) // st + 1) 
        for s, p, st in zip(raw.shape, patch_size, stride)
    ])
    n_bytes = 2 * n_patches_estimate * np.prod(patch_size) * 4  # float32
    _memory_check(n_bytes)
    
    # Create enhanced preprocessor
    pp = SPENDPreprocessor(
        permute_axis=permute_axis,
        pad_mode=pad_mode,
        patch_size=patch_size,
        stride=stride,
        rotate=rotate,
        flip=flip,
        seed=seed
    )
    
    # Add normalization and filtering
    pp.normalization = normalization
    pp.patch_filter = patch_filter
    
    X, Y = pp.run(raw)
    
    if verbose:
        print(f'Generated {X.shape[0]} patches of shape {X.shape[1:]}')
        print(f'X range: [{X.min():.3f}, {X.max():.3f}]')
        print(f'Y range: [{Y.min():.3f}, {Y.max():.3f}]')
        print('='*50)
    
    return X, Y


def create_spend_dataset_enhanced(
    raw: Array,
    permute_axis: AxisLike = "w",
    pad_mode: str = "drop",
    patch_size: Tuple[int, int, int] = (64, 64, 16),
    steps_per_epoch: int = 1000,
    seed: Optional[int] = None,
    to_channels_first: bool = False,
    normalization: Optional[Callable] = norm_percentiles(),
    verbose: bool = True
) -> "SPENDDataset":
    """Create enhanced SPENDDataset with normalization and proper augmentation.
    
    Parameters
    ----------
    raw : Array
        Raw hyperspectral data (x, y, w)
    permute_axis : AxisLike
        Axis along which to permute ("x", "y", "w" or 0/1/2)
    pad_mode : str
        How to handle odd length: "drop" or "reflect"
    patch_size : Tuple[int, int, int]
        3D patch size (px, py, pw)
    steps_per_epoch : int
        Number of random patches per epoch
    seed : Optional[int]
        Random seed for reproducible augmentations
    to_channels_first : bool
        If True, return (C,H,W), else (H,W,C)
    normalization : Optional[Callable]
        Normalization function (default: percentile normalization)
    verbose : bool
        Print progress and statistics
        
    Returns
    -------
    SPENDDataset
        Dataset that generates random patches with proper X,Y orientation matching
    """
    if verbose:
        print(f"Creating enhanced SPEND dataset:")
        print(f"  Raw shape: {raw.shape}")
        print(f"  Patch size: {patch_size}")
        print(f"  Steps per epoch: {steps_per_epoch}")
        print(f"  Normalization: {'Yes' if normalization else 'No'}")
        print(f"  Seed: {seed}")
    
    # Do permutation
    pp = SPENDPreprocessor(permute_axis=permute_axis, pad_mode=pad_mode)
    inp, tgt = pp.permute(raw)
    
    # Create dataset
    dataset = SPENDDataset(
        inp, tgt,
        patch_size=patch_size,
        steps_per_epoch=steps_per_epoch,
        seed=seed,
        to_channels_first=to_channels_first,
        normalization=normalization
    )
    
    if verbose:
        print(f"Dataset created successfully with {len(dataset)} samples per epoch")
    
    return dataset


if __name__ == "__main__":
    # Minimal smoke test
    raw = np.random.randn(128, 128, 31).astype(np.float32)
    X, Y = preprocess_spend(raw, permute_axis="w", patch_size=(64, 64, 8), stride=(32, 32, 8), seed=42)
    print("X patches:", X.shape, "Y patches:", Y.shape)
