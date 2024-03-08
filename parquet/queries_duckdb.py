"""Example showing how to query parquet files using duckdb."""

from pathlib import Path

import dataset
import duckdb


conn = duckdb.connect()


def create_table(name):
    """Create a duckdb table from a parquet file.

    Args:
        name: Name of the file without the .parquet suffix
    """
    data_dir = Path(__file__).parent / "dataset"
    file_path = str(data_dir / f"{name}.parquet")
    query = (
        f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM '{file_path}'"  # noqa: S608
    )
    conn.execute(query)


def create_tables():
    """Create all example tables."""
    create_table("customers")
    create_table("orders")
    create_table("products")
    create_table("details")
    create_table("categories")


def get_customer_orders(customer):
    """Get the orders for a given customer.

    Args:
        customer: The customer to return orders for.

    Returns:
        A dataframe with the products ordered by the customer.
    """
    query_str = f"""SELECT
        c.FirstName,
        p.ProductName
        FROM customers AS c
        JOIN orders AS o ON c.CustomerID = o.CustomerID
        JOIN details AS d ON o.OrderID = d.OrderID
        JOIN products AS p ON d.ProductID = p.ProductID
        WHERE c.FirstName = '{customer}'
    """

    return conn.execute(query_str).df()


if __name__ == "__main__":
    dataset.create_parquet_dataset()
    create_tables()

    customer_name = "Alice"
    print(f"Getting the products ordered by {customer_name}:")
    result = get_customer_orders(customer_name)
    print(result)
