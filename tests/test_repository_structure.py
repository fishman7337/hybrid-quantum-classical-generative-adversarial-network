from __future__ import annotations

from pathlib import Path

REQUIRED_DIRECTORIES = [
    "configs",
    "data",
    "data/raw",
    "data/processed",
    "docs",
    "models",
    "notebooks",
    "notebooks/legacy",
    "papers",
    "papers/arxiv-source",
    "papers/arxiv-source/Images",
    "papers/singapore-polytechnic-ca2",
    "papers/singapore-polytechnic-ca2/chapters",
    "papers/singapore-polytechnic-ca2/exp",
    "papers/singapore-polytechnic-ca2/exp/ch-Rice",
    "papers/singapore-polytechnic-ca2/pic",
    "papers/singapore-polytechnic-ca2/pic/ch-Intro",
    "papers/singapore-polytechnic-ca2/pic/ch-Noodle",
    "papers/singapore-polytechnic-ca2/pic/ch-Rice",
    "reports",
    "reports/figures",
    "scripts",
    "src",
    "src/hqcgan",
    "tests",
]


def test_each_project_directory_has_readme() -> None:
    missing = [
        directory for directory in REQUIRED_DIRECTORIES if not Path(directory, "README.md").exists()
    ]

    assert missing == []


def test_expected_research_artifacts_exist() -> None:
    assert Path("notebooks/Quantum-GAN.ipynb").exists()
    assert Path("notebooks/legacy/DELE_CA2_C.ipynb").exists()
    assert Path("papers/singapore-polytechnic-ca2/main.tex").exists()
    assert Path("papers/singapore-polytechnic-ca2/main.pdf").exists()
    assert Path("papers/arxiv-source/conference_101719.tex").exists()
    assert Path("papers/arxiv-source/2508.09209v2.pdf").exists()
    assert Path("papers/arxiv-source/HQCGAN-arXiv-2508.09209v1.pdf").exists()
