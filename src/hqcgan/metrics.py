"""Numerical metrics used by the HQCGAN experiments."""

from __future__ import annotations

import numpy as np
from scipy import linalg


def _as_2d_array(values: np.ndarray, name: str) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 2:
        msg = f"{name} must be a 2D array."
        raise ValueError(msg)
    return array


def _as_vector(values: np.ndarray, name: str) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64).reshape(-1)
    if array.ndim != 1:
        msg = f"{name} must be one-dimensional."
        raise ValueError(msg)
    return array


def frechet_distance_from_statistics(
    mu_real: np.ndarray,
    sigma_real: np.ndarray,
    mu_fake: np.ndarray,
    sigma_fake: np.ndarray,
    eps: float = 1e-6,
) -> float:
    """Compute the Frechet distance between two Gaussian feature summaries."""
    mu_real = _as_vector(mu_real, "mu_real")
    mu_fake = _as_vector(mu_fake, "mu_fake")
    sigma_real = _as_2d_array(sigma_real, "sigma_real")
    sigma_fake = _as_2d_array(sigma_fake, "sigma_fake")

    if mu_real.shape != mu_fake.shape:
        msg = "Mean vectors must have matching shapes."
        raise ValueError(msg)
    if sigma_real.shape != sigma_fake.shape:
        msg = "Covariance matrices must have matching shapes."
        raise ValueError(msg)
    if sigma_real.shape[0] != sigma_real.shape[1]:
        msg = "Covariance matrices must be square."
        raise ValueError(msg)

    diff = mu_real - mu_fake
    covmean = linalg.sqrtm(sigma_real @ sigma_fake)

    if not np.isfinite(covmean).all():
        offset = np.eye(sigma_real.shape[0]) * eps
        covmean = linalg.sqrtm((sigma_real + offset) @ (sigma_fake + offset))

    if np.iscomplexobj(covmean):
        covmean = covmean.real

    distance = diff @ diff + np.trace(sigma_real + sigma_fake - 2.0 * covmean)
    return float(max(distance, 0.0))


def polynomial_kernel_mmd(
    real_features: np.ndarray,
    fake_features: np.ndarray,
    degree: int = 3,
    gamma: float | None = None,
    coef0: float = 1.0,
) -> float:
    """Estimate KID-style squared MMD with a polynomial kernel."""
    real_features = _as_2d_array(real_features, "real_features")
    fake_features = _as_2d_array(fake_features, "fake_features")

    if real_features.shape[1] != fake_features.shape[1]:
        msg = "Feature dimensions must match."
        raise ValueError(msg)
    if real_features.shape[0] < 2 or fake_features.shape[0] < 2:
        msg = "At least two samples per set are required for unbiased MMD."
        raise ValueError(msg)

    feature_dim = real_features.shape[1]
    scale = gamma if gamma is not None else 1.0 / feature_dim

    k_xx = (scale * real_features @ real_features.T + coef0) ** degree
    k_yy = (scale * fake_features @ fake_features.T + coef0) ** degree
    k_xy = (scale * real_features @ fake_features.T + coef0) ** degree

    np.fill_diagonal(k_xx, 0.0)
    np.fill_diagonal(k_yy, 0.0)

    m = real_features.shape[0]
    n = fake_features.shape[0]
    return float(k_xx.sum() / (m * (m - 1)) + k_yy.sum() / (n * (n - 1)) - 2 * k_xy.mean())
