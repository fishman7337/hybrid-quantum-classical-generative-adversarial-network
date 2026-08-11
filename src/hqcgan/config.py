"""Configuration helpers for HQCGAN experiments."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ResearchMetadata:
    """Static provenance for the research project."""

    title: str = (
        "Quantum-Enhanced Generative Adversarial Networks: Comparative Analysis "
        "of Classical and Hybrid Quantum-Classical Generative Adversarial Networks"
    )
    short_name: str = "HQCGAN"
    author: str = "Goh Kun Ming"
    author_orcid: str = "https://orcid.org/0009-0008-7666-781X"
    institution: str = "Singapore Polytechnic, School of Computing"
    programme: str = "Diploma in Applied AI and Analytics"
    module: str = "Deep Learning (ST1504), CA2 Part C"
    academic_period: str = "AY25/26 Year 2 Semester 1"
    supervising_lecturer: str = "Lecturer Gerald Chua Deng Xiang"
    arxiv_url: str = "https://arxiv.org/abs/2508.09209"
    doi: str = "10.48550/arXiv.2508.09209"


@dataclass(frozen=True)
class ExperimentConfig:
    """Minimal experiment configuration shared by code, notebooks, and tests."""

    dataset: str = "mnist-binary-0-1"
    classes: tuple[int, int] = (0, 1)
    epochs: int = 150
    batch_size: int = 64
    latent_dim: int = 100
    fid_samples: int = 500
    qubits: tuple[int, ...] = (3, 5, 7)
    random_seed: int = 42
    model_dir: Path = field(default_factory=lambda: Path("models"))
    figure_dir: Path = field(default_factory=lambda: Path("reports/figures"))

    def validate(self) -> None:
        """Raise ValueError when the configuration is internally inconsistent."""
        if len(self.classes) != 2:
            msg = "This research configuration expects exactly two MNIST classes."
            raise ValueError(msg)
        if self.epochs <= 0:
            msg = "epochs must be positive."
            raise ValueError(msg)
        if self.batch_size <= 0:
            msg = "batch_size must be positive."
            raise ValueError(msg)
        if self.latent_dim <= 0:
            msg = "latent_dim must be positive."
            raise ValueError(msg)
        if self.fid_samples <= 0:
            msg = "fid_samples must be positive."
            raise ValueError(msg)
        if not self.qubits or any(q <= 0 for q in self.qubits):
            msg = "qubits must contain positive integers."
            raise ValueError(msg)

    @classmethod
    def from_mapping(cls, values: dict[str, Any]) -> ExperimentConfig:
        """Build a config from a nested or flat mapping."""
        data = values.get("data", {})
        training = values.get("training", {})
        classical = values.get("classical_gan", {})
        hqcgan = values.get("hqcgan", {})
        reproducibility = values.get("reproducibility", {})
        artifacts = values.get("artifacts", {})

        config = cls(
            dataset=data.get("dataset", values.get("dataset", cls.dataset)),
            classes=tuple(data.get("classes", values.get("classes", cls.classes))),
            epochs=int(training.get("epochs", values.get("epochs", cls.epochs))),
            batch_size=int(training.get("batch_size", values.get("batch_size", cls.batch_size))),
            latent_dim=int(classical.get("latent_dim", values.get("latent_dim", cls.latent_dim))),
            fid_samples=int(data.get("fid_samples", values.get("fid_samples", cls.fid_samples))),
            qubits=tuple(hqcgan.get("qubits", values.get("qubits", cls.qubits))),
            random_seed=int(
                reproducibility.get("random_seed", values.get("random_seed", cls.random_seed))
            ),
            model_dir=Path(artifacts.get("model_dir", values.get("model_dir", "models"))),
            figure_dir=Path(
                artifacts.get("figure_dir", values.get("figure_dir", "reports/figures"))
            ),
        )
        config.validate()
        return config


def load_experiment_config(path: str | Path) -> ExperimentConfig:
    """Load an experiment config from YAML."""
    with Path(path).open("r", encoding="utf-8") as handle:
        values = yaml.safe_load(handle) or {}
    if not isinstance(values, dict):
        msg = f"Expected YAML mapping in {path!s}."
        raise ValueError(msg)
    return ExperimentConfig.from_mapping(values)
