# Contributing

Thank you for improving this research repository. Contributions should make the
work easier to reproduce, audit, or extend.

## Development Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Install experiment dependencies only when you need to run training:

```powershell
python -m pip install -e ".[experiment,quantum]"
```

## Contribution Rules

- Keep paper source archives intact unless a change explicitly targets a new
  paper version.
- Do not commit `.env`, raw datasets, generated checkpoints, local databases,
  or long-running experiment outputs.
- Add or update a folder `README.md` when introducing a new directory.
- Prefer reusable code in `src/hqcgan/` over copying notebook-only logic.
- Update `configs/` and `docs/reproducibility.md` when experiment defaults
  change.
- Add focused tests for reusable utilities and lightweight behavior.

## Quality Checks

Run these before submitting a change:

```powershell
python -m ruff check .
python -m pytest
python scripts/validate_notebooks.py
```

Long GPU or quantum-simulation runs are not required for normal pull requests.
Record those results in `reports/` or an external artifact store instead.
