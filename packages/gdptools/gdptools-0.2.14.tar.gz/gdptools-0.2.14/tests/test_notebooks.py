"""Test runs each notebook in the docs/Examples directory."""

import os
import pytest

# Only run if certain packages are installed
pynhd = pytest.importorskip("pynhd")
hvplot = pytest.importorskip("hvplot")
nbformat = pytest.importorskip("nbformat")
nbconvert = pytest.importorskip("nbconvert")

from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError  # noqa


EXAMPLE_DIR = "docs/Examples"

# Collect all notebook paths
NOTEBOOK_DIRS = [os.path.join(EXAMPLE_DIR, f) for f in os.listdir(EXAMPLE_DIR)]

notebook_paths = []

for p in NOTEBOOK_DIRS:
    for f in os.listdir(p):
        if f.endswith(".ipynb"):
            # Don't run the Merra 2 demo notebook until its fixedS
            if f.endswith("Merra-2-example.ipynb"):
                print("Skipping the Merra-2 notebook")
                continue
            else:
                notebook_paths.append(os.path.join(p, f))


class CustomExecutePreprocessor(ExecutePreprocessor):
    """Executes all the cells in a notebook, and creates a print statement after each successful cell execution."""

    def preprocess_cell(self, cell, resources, index):
        """Print a statement before running each cell."""
        print(f"Running cell {index + 1}...")
        result = super().preprocess_cell(cell, resources, index)
        print(f"Cell {index + 1} ran successfully.")
        return result


@pytest.mark.parametrize("notebook_path", notebook_paths)
def test_notebook_execution(notebook_path):
    """Test function to execute each notebook in the repo."""
    with open(notebook_path) as f:
        notebook = nbformat.read(f, as_version=4)

    ep = CustomExecutePreprocessor(timeout=600, kernel_name="python3")

    try:
        ep.preprocess(notebook, {"metadata": {"path": os.path.dirname(notebook_path)}})
    except CellExecutionError as e:
        raise RuntimeError(f"Error executing the notebook '{notebook_path}': {e}") from e
