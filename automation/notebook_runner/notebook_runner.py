import sys

import nbformat
from dapla.git import repo_root_dir
from nbconvert.preprocessors import ExecutePreprocessor


python_executable_path = sys.executable

print("Path to the current Python executable:", python_executable_path)

root = repo_root_dir()
# Define the list of notebook files in the desired execution order
notebook_files = [
    root / "automation/notebook_runner/notebooks/common_data.ipynb",  # First notebook
    root / "automation/notebook_runner/notebooks/notebook1.ipynb",  # First notebook
    root / "automation/notebook_runner/notebooks/notebook2.ipynb",  # Second notebook
    # Add more notebooks in the desired order
]

# Loop through and execute each notebook
for notebook_file in notebook_files:
    with open(notebook_file) as f:
        notebook = nbformat.read(f, as_version=4)

    # Create an execution preprocessor
    ep = ExecutePreprocessor(
        timeout=600, kernel_name="python3"
    )  # Adjust timeout as needed

    # Execute the notebook
    ep.preprocess(notebook, {"metadata": {"path": "./"}})  # Set the path accordingly

    # Save the executed notebook
    with open(notebook_file, "w", encoding="utf-8") as f:
        nbformat.write(notebook, f)
