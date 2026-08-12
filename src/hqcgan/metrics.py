"""Numerical metrics used by the HQCGAN experiments."""

from __future__ import annotations

import numpy as np
from scipy import linalg

_COVARIANCE_RTOL = 1e-8
_COVARIANCE_ATOL = 1e-10
_SQRTM_IMAGINARY_RTOL = 1e-8


def _as_2d_array(values: np.ndarray, name: str) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 2:
        msg = f"{name} must be a 2D array."
        raise ValueError(msg)
    if not np.isfinite(array).all():
        msg = f"{name} must contain only finite values."
        raise ValueError(msg)
    return array


def _as_vector(values: np.ndarray, name: str) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 1:
        msg = f"{name} must be one-dimensional."
        raise ValueError(msg)
    if not np.isfinite(array).all():
        msg = f"{name} must contain only finite values."
        raise ValueError(msg)
    return array


def _validate_covariance(matrix: np.ndarray, name: str) -> None:
    """Require a symmetric positive-semidefinite covariance matrix."""
    if matrix.shape[0] != matrix.shape[1]:
        msg = f"{name} must be square."
        raise ValueError(msg)
    if not np.allclose(
        matrix,
        matrix.T,
        rtol=_COVARIANCE_RTOL,
        atol=_COVARIANCE_ATOL,
    ):
        msg = f"{name} must be symmetric."
        raise ValueError(msg)

    symmetric_matrix = (matrix + matrix.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(symmetric_matrix)
    scale = max(1.0, float(np.max(np.abs(eigenvalues))))
    if float(np.min(eigenvalues)) < -_COVARIANCE_ATOL * scale:
        msg = f"{name} must be positive semidefinite."
        raise ValueError(msg)


def _discard_negligible_imaginary_part(values: np.ndarray) -> np.ndarray:
    """Return a real matrix unless a complex square-root residual is material."""
    if not np.iscomplexobj(values):
        return values

    real_values = values.real
    imaginary_scale = float(np.max(np.abs(values.imag)))
    real_scale = max(1.0, float(np.max(np.abs(real_values))))
    if imaginary_scale > _SQRTM_IMAGINARY_RTOL * real_scale:
        msg = "Covariance matrix square root has a material complex component."
        raise ValueError(msg)
    return real_values


def frechet_distance_from_statistics(
    mu_real: np.ndarray,
    sigma_real: np.ndarray,
    mu_fake: np.ndarray,
    sigma_fake: np.ndarray,
    eps: float = 1e-6,
) -> float:
    """Compute the Frechet distance between two Gaussian feature summaries."""
    if eps <= 0 or not np.isfinite(eps):
        msg = "eps must be a positive finite number."
        raise ValueError(msg)

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
    _validate_covariance(sigma_real, "sigma_real")
    _validate_covariance(sigma_fake, "sigma_fake")
    if sigma_real.shape[0] != mu_real.shape[0]:
        msg = "Covariance dimensions must match the mean-vector length."
        raise ValueError(msg)

    diff = mu_real - mu_fake
    covmean = linalg.sqrtm(sigma_real @ sigma_fake)

    if not np.isfinite(covmean).all():
        offset = np.eye(sigma_real.shape[0]) * eps
        covmean = linalg.sqrtm((sigma_real + offset) @ (sigma_fake + offset))

    if not np.isfinite(covmean).all():
        msg = "Covariance matrix square root must contain only finite values."
        raise ValueError(msg)
    covmean = _discard_negligible_imaginary_part(covmean)

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
    if real_features.shape[1] == 0:
        msg = "Feature arrays must contain at least one feature column."
        raise ValueError(msg)
    if not isinstance(degree, int) or degree <= 0:
        msg = "degree must be a positive integer."
        raise ValueError(msg)
    if gamma is not None and (gamma <= 0 or not np.isfinite(gamma)):
        msg = "gamma must be a positive finite number when supplied."
        raise ValueError(msg)
    if not np.isfinite(coef0):
        msg = "coef0 must be finite."
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
