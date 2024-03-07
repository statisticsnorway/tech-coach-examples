from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq


def create_files() -> None:
    """Create parquet file stored with different index options."""
    data_dir = Path(__file__).parent / "dataset"
    customers_df = pd.read_csv(data_dir / "customers.csv")
    customers_df.to_parquet(data_dir / "customers-no-index.parquet", index=False)
    customers_df.to_parquet(data_dir / "customers-with-index.parquet", index=True)
    customers_df.to_parquet(data_dir / "customers-def-index.parquet", index=None)


def load_file(name: str) -> pq.ParquetFile:
    """Read the given dataset from a parquet file.

    Args:
        name: Name of the file without the .parquet suffix
    """
    data_dir = Path(__file__).parent / "dataset"
    file_path = data_dir / f"{name}.parquet"
    return pq.ParquetFile(file_path)


if __name__ == "__main__":
    # create_files()
    parquet_file = load_file("customers-def-index")
    print(parquet_file.schema)
    print(parquet_file.metadata)
    custom_metadata = parquet_file.metadata.metadata
    if custom_metadata:
        print("\nCustom Metadata:")
        for key, value in custom_metadata.items():
            print(f"{key.decode('utf-8')}: {value.decode('utf-8')}")
    else:
        print("\nNo custom metadata found.")
