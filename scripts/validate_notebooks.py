"""Validate repository notebooks without executing long-running cells."""

from __future__ import annotations

from pathlib import Path

import nbformat

REQUIRED_MARKDOWN_TERMS = ("research context", "reproducibility", "metric")


def validate_notebook(path: Path) -> list[str]:
    """Return validation problems for a notebook."""
    problems: list[str] = []
    notebook = nbformat.read(path, as_version=4)
    _, notebook = nbformat.validator.normalize(notebook)

    nbformat.validate(notebook)

    markdown_text = "\n".join(
        "".join(cell.get("source", "")).lower()
        for cell in notebook.cells
        if cell.get("cell_type") == "markdown"
    )

    for term in REQUIRED_MARKDOWN_TERMS:
        if term not in markdown_text:
            problems.append(f"{path}: missing markdown discussion for '{term}'")

    if not any(cell.get("cell_type") == "code" for cell in notebook.cells):
        problems.append(f"{path}: expected at least one code cell")

    for cell_index, cell in enumerate(notebook.cells, start=1):
        if cell.get("cell_type") != "code":
            continue
        for output in cell.get("outputs", []):
            if output.get("output_type") != "error":
                continue
            error_name = output.get("ename", "Exception")
            error_value = output.get("evalue", "")
            detail = f": {error_value}" if error_value else ""
            problems.append(
                f"{path}: code cell {cell_index} stores execution error {error_name}{detail}"
            )

    return problems


def main() -> int:
    """Validate every research notebook and return a process exit code."""
    notebook_paths = sorted(Path("notebooks").glob("*.ipynb"))
    if not notebook_paths:
        print("No notebooks found.")
        return 0

    problems: list[str] = []
    for path in notebook_paths:
        problems.extend(validate_notebook(path))

    if problems:
        for problem in problems:
            print(problem)
        return 1

    for path in notebook_paths:
        print(f"Validated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
