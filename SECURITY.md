# Security Policy

This project is a research repository, not a production service. The main
security risks are accidental credential exposure, unsafe data handling, and
unreviewed executable notebooks.

## Supported Versions

Security fixes apply to the current main research branch.

## Reporting

Report concerns privately to the repository maintainer where possible. Include
the affected file, a short impact description, and steps to reproduce.

## Handling Secrets

- Put local values in `.env`; use `.env.example` as the public template.
- Never commit API keys, cloud credentials, database URLs, or private dataset
  paths.
- Rotate any secret that was committed or printed in notebook output.

## Notebook Safety

Review notebook cells before execution, especially when they download data,
load serialized models, or run shell commands.
