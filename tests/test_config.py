from __future__ import annotations

from pathlib import Path

import pytest

from hqcgan.config import ExperimentConfig, ResearchMetadata, load_experiment_config


def test_research_metadata_contains_public_identifiers() -> None:
    metadata = ResearchMetadata()

    assert metadata.short_name == "HQCGAN"
    assert "2508.09209" in metadata.arxiv_url
    assert metadata.author_orcid.endswith("0009-0008-7666-781X")


def test_experiment_config_defaults_are_valid() -> None:
    config = ExperimentConfig()

    config.validate()

    assert config.classes == (0, 1)
    assert config.qubits == (3, 5, 7)
    assert config.figure_dir == Path("reports/figures")


def test_experiment_config_rejects_invalid_epochs() -> None:
    with pytest.raises(ValueError, match="epochs"):
        ExperimentConfig(epochs=0).validate()


def test_load_experiment_config_example() -> None:
    config = load_experiment_config("configs/experiment.example.yaml")

    assert config.dataset == "mnist-binary-0-1"
    assert config.epochs == 150
    assert config.qubits == (3, 5, 7)
