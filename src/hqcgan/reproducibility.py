"""Reproducibility helpers."""

from __future__ import annotations

import os
import random
from pathlib import Path


def seed_everything(
    seed: int = 42,
    deterministic_tensorflow: bool = False,
    seed_tensorflow: bool = False,
) -> int:
    """Seed common Python and NumPy RNGs, with optional TensorFlow seeding."""
    if seed < 0:
        msg = "seed must be non-negative."
        raise ValueError(msg)

    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)

    try:
        import numpy as np
    except ImportError:
        np = None

    if np is not None:
        np.random.seed(seed)

    if deterministic_tensorflow:
        os.environ["TF_DETERMINISTIC_OPS"] = "1"

    if seed_tensorflow or deterministic_tensorflow:
        try:
            import tensorflow as tf
        except Exception:
            # TensorFlow is optional and may be installed with incompatible native wheels.
            tf = None

    if (seed_tensorflow or deterministic_tensorflow) and tf is not None:
        tf.random.set_seed(seed)

    return seed


def project_path(*parts: str, root: str | Path | None = None) -> Path:
    """Resolve a path relative to the project root or a supplied root."""
    base = Path(root) if root is not None else Path.cwd()
    return base.joinpath(*parts).resolve()
