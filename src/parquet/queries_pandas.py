"""Example showing how to query parquet files using pandas."""

from pathlib import Path

import dataset
import pandas as pd


def load_table(name):
    """Read the given dataset from a parquet file.

    Args:
        name: Name of the file without the .parquet suffix
    """
    data_dir = Path(__file__).parent / "dataset"
    file_path = data_dir / f"{name}.parquet"
    return pd.read_parquet(file_path)


def get_customer_orders(customer):
    """Get the orders for a given customer.

    Args:
        customer: The customer to return orders for.

    Returns:
        A dataframe with the products ordered by the customer.
    """
    # Load tables
    customers = load_table("customers")
    orders = load_table("orders")
    details = load_table("details")
    products = load_table("products")

    # Merge tables
    df = (
        customers.merge(orders, on="CustomerID")
        .merge(details, on="OrderID")
        .merge(products, on="ProductID")
    )

    # Filter customer and return dataframe with FirstName and ProductName columns
    return df[df["FirstName"] == customer][["FirstName", "ProductName"]]


if __name__ == "__main__":
    dataset.create_parquet_dataset()

    customer_name = "Alice"
    print(f"Getting the products ordered by {customer_name}:")
    result = get_customer_orders(customer_name)
    print(result)
