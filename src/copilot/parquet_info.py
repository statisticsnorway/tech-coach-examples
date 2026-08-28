"""This module prints metadata and statistics about a parquet file.

Use the output as part of the AI-prompt when generating synthetic data
from the dataset. It prints:

- The Parquet schema (column names, types, and nullability)
- Basic statistics for numeric columns
- Basic statistics for object/category columns (if any exist)
- Null-value counts per column
- A small sample of the dataset
"""

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Vis alle kolonner og rader
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_rows", None)


def inspect_parquet(path: str, n_rows_sample: int = 10):
    # les filens schema uten å laste hele datasettet
    table = pq.read_table(path, memory_map=True)
    schema: pa.Schema = table.schema
    print("=== Parquet schema ===")
    for field in schema:
        print(f"  · {field.name} : {field.type} (nullable={field.nullable})")
    print()

    # last inn et lite utvalg for statistikk og visning
    df = pd.read_parquet(path, engine="pyarrow", columns=schema.names)

    # Generelle statistikker for numeriske og ikke-numeriske kolonner
    print("=== Basic statistics (numeric columns) ===")
    num_cols = df.select_dtypes(include="number")
    if len(num_cols.columns) > 0:
        print(num_cols.describe())
    else:
        print("No numeric columns in this dataset.")
    print()

    print("=== Basic statistics (object / category columns) ===")
    obj_cols = df.select_dtypes(include=["object", "category"])
    if len(obj_cols.columns) > 0:
        print(obj_cols.describe())
    else:
        print("No object or category columns in this dataset.")
    print()

    # null-verdier per kolonne
    null_counts = df.isna().sum()
    print("=== Null counts per column ===")
    print(null_counts[null_counts > 0])
    print()

    print(f"=== Sample first {n_rows_sample} rows ===")
    print(df.head(n_rows_sample))
    print()


if __name__ == "__main__":
    # To get access to the example file, use dapla-felles as Dapla Team in Daplalab
    example = (
        "/buckets/produkt/tech-coach/metstat/inndata/frost/weather_stations_v1.parquet"
    )
    inspect_parquet(example, n_rows_sample=20)
