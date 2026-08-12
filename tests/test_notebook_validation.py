"""Tests for committed notebook validation."""

from pathlib import Path

import nbformat

from scripts.validate_notebooks import validate_notebook


def test_validator_rejects_stored_execution_errors(tmp_path: Path) -> None:
    """Reject stored tracebacks while accepting the same clean notebook."""
    notebook = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_markdown_cell(
                "Research context, reproducibility, and metric documentation."
            ),
            nbformat.v4.new_code_cell("answer = 42"),
        ]
    )
    notebook_path = tmp_path / "research.ipynb"
    nbformat.write(notebook, notebook_path)
    assert validate_notebook(notebook_path) == []

    notebook.cells[1].outputs = [
        nbformat.v4.new_output(
            output_type="error",
            ename="ValueError",
            evalue="invalid experiment state",
            traceback=["ValueError: invalid experiment state"],
        )
    ]
    nbformat.write(notebook, notebook_path)

    assert validate_notebook(notebook_path) == [
        f"{notebook_path}: code cell 2 stores execution error ValueError: invalid experiment state"
    ]
