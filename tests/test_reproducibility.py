from __future__ import annotations

import random

import numpy as np
import pytest

from hqcgan.reproducibility import project_path, seed_everything


def test_seed_everything_repeats_python_and_numpy_rngs() -> None:
    seed_everything(123)
    first_python = random.random()
    first_numpy = np.random.random()

    seed_everything(123)

    assert random.random() == first_python
    assert np.random.random() == first_numpy


def test_seed_everything_rejects_negative_seed() -> None:
    with pytest.raises(ValueError, match="seed"):
        seed_everything(-1)


def test_project_path_resolves_from_supplied_root(tmp_path) -> None:
    resolved = project_path("models", root=tmp_path)

    assert resolved == tmp_path.joinpath("models").resolve()
