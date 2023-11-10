from pathlib import Path

import pandas as pd


def create_parquet_dataset():
    """Create the dataset parquet files from cvs files."""
    data_dir = Path(__file__).parent / "dataset"
    customers_df = pd.read_csv(data_dir / "customers.csv")
    customers_df.to_parquet(data_dir / "customers.parquet")

    orders_df = pd.read_csv(data_dir / "orders.csv")
    orders_df.to_parquet(data_dir / "orders.parquet")

    products_df = pd.read_csv(data_dir / "products.csv")
    products_df.to_parquet(data_dir / "products.parquet")

    orderdetails_df = pd.read_csv(data_dir / "details.csv")
    orderdetails_df.to_parquet(data_dir / "details.parquet")

    categories_df = pd.read_csv(data_dir / "categories.csv")
    categories_df.to_parquet(data_dir / "categories.parquet")


if __name__ == "__main__":
    create_parquet_dataset()
