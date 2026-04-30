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


def test_polynomial_kernel_mmd_requires_matching_feature_dimensions() -> None:
    with pytest.raises(ValueError, match="Feature dimensions"):
        polynomial_kernel_mmd(np.ones((3, 2)), np.ones((3, 4)))
