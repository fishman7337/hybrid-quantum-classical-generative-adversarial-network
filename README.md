# Quantum-Enhanced GANs (HQCGAN Research)

Research repository for **Quantum-Enhanced Generative Adversarial Networks:
Comparative Analysis of Classical and Hybrid Quantum-Classical Generative
Adversarial Networks**.

This work was completed under Singapore Polytechnic, School of Computing,
Diploma in Applied AI and Analytics, for the Deep Learning module
(`ST1504`), CA2 Part C, AY25/26 Year 2 Semester 1.

Author: Goh Kun Ming, DAAA student,
[ORCID 0009-0008-7666-781X](https://orcid.org/0009-0008-7666-781X)

Supervising lecturer: Lecturer Gerald Chua Deng Xiang

Public paper: [arXiv:2508.09209](https://arxiv.org/abs/2508.09209)

## Evidence and interpretation

| Evidence-backed measure | Current repository evidence |
| --- | --- |
| Experiment matrix | A classical GAN is compared with **3-, 5-, and 7-qubit** HQCGAN variants on binary MNIST digits **0 and 1**. |
| Reproducibility gate | **13 tests** validate configuration, metrics, repository structure, reproducibility helpers, and stored-error rejection. |

The notebook now defaults to a bounded smoke study and requires `QGAN_FULL_STUDY=1` for the long optimisation. This project is distinct from the separate quantum-computing sustainability report and does not support the report's power-consumption claims.

## Purpose

The project studies whether hybrid quantum-classical GANs can use noisy
parameterised quantum circuits as latent priors for image generation. The
experiments compare a classical GAN against HQCGAN variants with 3, 5, and 7
qubits on binary MNIST digits 0 and 1.

The original submission and the arXiv paper source are preserved as immutable
paper artifacts under `papers/`. The notebook is retained under `notebooks/`,
and reusable helpers, tests, and MLOps conventions have been added around it.

## Repository Layout

```text
.
|-- .github/                 CI workflow configuration
|-- configs/                 Example experiment configuration
|-- data/                    Local data mount points, not committed
|-- docs/                    Research, reproduction, and MLOps notes
|-- models/                  Local model checkpoints, not committed
|-- notebooks/               Jupyter notebooks
|-- papers/                  Submitted and arXiv paper source bundles
|-- reports/                 Local generated figures and reports
|-- scripts/                 Utility scripts
|-- src/hqcgan/              Reusable Python utilities
`-- tests/                   Pytest suite
```

Every research/content folder contains a `README.md` describing its role.
Automation-only folders such as `.github/` intentionally contain only workflow
configuration so GitHub does not render a folder README in place of the root
project README during navigation.

## Quick Start

Create an environment and install the lightweight development dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest
```

For full experiment work, install the optional ML and quantum dependencies:

```powershell
python -m pip install -e ".[experiment,quantum,dev]"
```

Then copy `.env.example` to `.env` and adjust local paths if needed.

## Research Artifacts

- `papers/singapore-polytechnic-ca2/` contains the expanded source package and
  PDF for the `ST1504` CA2 Part C submission.
- `papers/arxiv-source/` contains the expanded source package and PDF artifacts
  corresponding to the public arXiv paper.
- `notebooks/Quantum-GAN.ipynb` contains the exploratory GAN notebook with
  added markdown structure and corrected FID preprocessing notes.

## MLOps Summary

- Source code lives in `src/hqcgan/`.
- Reproducible settings are recorded in `configs/experiment.example.yaml`.
- Local data, checkpoints, and generated figures are intentionally ignored by
  git while their folders remain documented.
- CI runs notebook structure checks, unit tests, and static linting.
- Secrets and machine-specific paths belong in `.env`, never in source files.

See [docs/mlops.md](docs/mlops.md) and
[docs/reproducibility.md](docs/reproducibility.md) for the detailed workflow.

## Citation

Use the metadata in [CITATION.cff](CITATION.cff), or cite:

> Goh, K. M. (2025). Quantum-Enhanced Generative Adversarial Networks:
> Comparative Analysis of Classical and Hybrid Quantum-Classical Generative
> Adversarial Networks. arXiv:2508.09209.
> https://doi.org/10.48550/arXiv.2508.09209

## License

Code in this repository is released under the MIT License. Research narrative,
documentation, notebooks, and author-owned figures are made available under
CC BY 4.0 unless a specific artifact states otherwise. Third-party templates
inside preserved paper bundles retain their original licenses.
