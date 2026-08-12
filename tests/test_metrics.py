from __future__ import annotations

import numpy as np
import pytest

from hqcgan.metrics import frechet_distance_from_statistics, polynomial_kernel_mmd


def test_frechet_distance_is_zero_for_identical_statistics() -> None:
    mean = np.array([0.0, 1.0])
    covariance = np.eye(2)

    distance = frechet_distance_from_statistics(mean, covariance, mean, covariance)

    assert distance == pytest.approx(0.0, abs=1e-10)


def test_frechet_distance_increases_for_shifted_mean() -> None:
    covariance = np.eye(2)

    distance = frechet_distance_from_statistics(
        np.array([0.0, 0.0]),
        covariance,
        np.array([1.0, 0.0]),
        covariance,
    )

    assert distance == pytest.approx(1.0, abs=1e-8)


def test_frechet_distance_rejects_matrix_mean() -> None:
    with pytest.raises(ValueError, match="one-dimensional"):
        frechet_distance_from_statistics(
            np.ones((1, 2)),
            np.eye(2),
            np.ones(2),
            np.eye(2),
        )


def test_frechet_distance_rejects_covariance_dimension_mismatch() -> None:
    with pytest.raises(ValueError, match="mean-vector length"):
        frechet_distance_from_statistics(
            np.ones(2),
            np.eye(3),
            np.ones(2),
            np.eye(3),
        )


@pytest.mark.parametrize(
    ("covariance", "message"),
    [
        (np.array([[1.0, 0.5], [0.0, 1.0]]), "symmetric"),
        (np.array([[1.0, 2.0], [2.0, 1.0]]), "positive semidefinite"),
        (np.array([[1.0, np.inf], [np.inf, 1.0]]), "finite values"),
    ],
)
def test_frechet_distance_rejects_invalid_covariance_matrices(
    covariance: np.ndarray,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        frechet_distance_from_statistics(
            np.zeros(2),
            covariance,
            np.zeros(2),
            np.eye(2),
        )


def test_frechet_distance_rejects_material_complex_sqrtm_residual(monkeypatch) -> None:
    complex_root = np.array([[1.0 + 1e-3j, 0.0], [0.0, 1.0]])
    monkeypatch.setattr("hqcgan.metrics.linalg.sqrtm", lambda _matrix: complex_root)

    with pytest.raises(ValueError, match="material complex component"):
        frechet_distance_from_statistics(
            np.zeros(2),
            np.eye(2),
            np.zeros(2),
            np.eye(2),
        )


def test_frechet_distance_discards_negligible_complex_sqrtm_residual(monkeypatch) -> None:
    complex_root = np.array([[1.0 + 1e-12j, 0.0], [0.0, 1.0]])
    monkeypatch.setattr("hqcgan.metrics.linalg.sqrtm", lambda _matrix: complex_root)

    distance = frechet_distance_from_statistics(
        np.zeros(2),
        np.eye(2),
        np.zeros(2),
        np.eye(2),
    )

    assert distance == pytest.approx(0.0, abs=1e-10)


def test_polynomial_kernel_mmd_requires_matching_feature_dimensions() -> None:
    with pytest.raises(ValueError, match="Feature dimensions"):
        polynomial_kernel_mmd(np.ones((3, 2)), np.ones((3, 4)))


def test_polynomial_kernel_mmd_rejects_invalid_kernel_parameters() -> None:
    features = np.ones((3, 2))

    with pytest.raises(ValueError, match="degree"):
        polynomial_kernel_mmd(features, features, degree=0)
    with pytest.raises(ValueError, match="gamma"):
        polynomial_kernel_mmd(features, features, gamma=0.0)
