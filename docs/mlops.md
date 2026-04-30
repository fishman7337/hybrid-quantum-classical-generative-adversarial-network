# MLOps Notes

This repository uses lightweight MLOps conventions suitable for an academic
research project.

## Source Control Boundaries

Commit:

- Source code in `src/`
- Tests in `tests/`
- Reproducible configs in `configs/`
- Documentation in `docs/`
- Small paper source bundles in `papers/`

Do not commit:

- `.env`
- Raw datasets or generated processed datasets
- Model checkpoints
- Experiment tracker directories such as `mlruns/` or `wandb/`
- Local Optuna SQLite databases

## Experiment Tracking

The `.env.example` file includes optional `MLFLOW_TRACKING_URI` and
`WANDB_PROJECT` variables. If a tracker is used, record:

- Git commit hash or archive version
- Config file path
- Dataset version or preparation script
- Random seed
- Hardware and simulator backend
- Metrics, generated figures, and checkpoint paths

## CI Strategy

The CI workflow avoids long training and quantum simulation. It checks:

- Static linting with Ruff
- Unit tests with Pytest
- Notebook validity with `scripts/validate_notebooks.py`

Long-running validation should be handled by manual experiment runs or a
dedicated research compute workflow.

## Artifact Strategy

Use local folders during development:

- `models/` for checkpoints
- `reports/figures/` for plots
- `reports/` for run summaries

For publication-quality releases, attach artifacts to a tagged release or an
external archive with a DOI.
