GOAL: Generate a synthetic dataset based on an existing Parquet dataset.

Requirements:
- Target row_count = 100
- Keep same column names, datatypes and nullability
- For numeric columns: generate realistic values approximately in the same min-max or mean±10% range, maintain distribution shape (if known)
- For categorical columns: keep same value set, approximate same frequency distribution
- Preserve null (“missing”) proportion for each column
- The synthetic dataset must not contain any real sensitive identifiers—fully anonymized
- Use Python 3.12, pandas + pyarrow (or other specified libs)
- Format code with Black style
- The output file should be `synthetic_data.parquet`, same column order as original, no extra index column
- Include docstring at module and function level, modular design (e.g., a function `generate_synthetic_dataset(...)`)
- Provide logging of the process (e.g., row count, null counts per column) and a simple CLI (--rows, --output_path)

Schema & metadata (copy output from the parquet_info.py script below):

START PROMPT FOR COPILOT:
Please generate the Python code file based on the above schema and requirements.
End prompt.
