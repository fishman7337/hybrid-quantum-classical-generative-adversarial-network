# Reproducibility

## Environment

Use Python 3.10 or newer. The original notebook metadata records Python 3.8,
but the packaged tooling is configured for modern supported Python versions.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[experiment,quantum,dev]"
```

For CI-style checks only:

```powershell
python -m pip install -e ".[dev]"
python -m pytest
python scripts/validate_notebooks.py
```

## Configuration

Start from:

```text
configs/experiment.example.yaml
```

Record any run-specific changes in a copied config file or in your experiment
tracker. Do not overwrite the example with local machine paths.

## Data

The notebook uses Keras MNIST and filters digits 0 and 1. It balances classes
before training. Raw and processed local data files should stay out of git.

## Expected Long-Running Steps

Training GANs, computing FID/KID repeatedly, and simulating quantum circuits
can be slow. CI intentionally does not rerun the full experiments. CI verifies
that reusable utilities, notebook structure, and repository standards remain
healthy.

## Reproducibility Checklist

- Record Python version and dependency lock file if producing final results.
- Set `HQCGAN_RANDOM_SEED` or the config seed before a run.
- Preserve the exact config used for each reported figure.
- Store checkpoints under `models/` or external artifact storage.
- Store generated figures under `reports/figures/`.
- Document hardware, simulator backend, shot count, and noise model settings.
