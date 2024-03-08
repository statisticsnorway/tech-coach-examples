# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: tech-coach-examples
#     language: python
#     name: tech-coach-examples
# ---

# %%
import dapla as dp
import duckdb


conn = duckdb.connect()

# %%
customers = (
    "gs://ssb-prod-dapla-felles-data-delt/tech-coach/parquet-example/customers.parquet"
)
orders = (
    "gs://ssb-prod-dapla-felles-data-delt/tech-coach/parquet-example/orders.parquet"
)
products = (
    "gs://ssb-prod-dapla-felles-data-delt/tech-coach/parquet-example/products.parquet"
)
details = (
    "gs://ssb-prod-dapla-felles-data-delt/tech-coach/parquet-example/details.parquet"
)
categories = (
    "gs://ssb-prod-dapla-felles-data-delt/tech-coach/parquet-example/categories.parquet"
)

# %%
df_customers = dp.read_pandas(customers)
df_orders = dp.read_pandas(orders)
df_products = dp.read_pandas(products)
df_details = dp.read_pandas(details)
df_categories = dp.read_pandas(categories)
df_customers.head()


# %%
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
        FROM df_customers AS c
        JOIN df_orders AS o ON c.CustomerID = o.CustomerID
        JOIN df_details AS d ON o.OrderID = d.OrderID
        JOIN df_products AS p ON d.ProductID = p.ProductID
        WHERE c.FirstName = '{customer}'
    """

    return conn.execute(query_str).df()


# %%
print(duckdb.query("SELECT * FROM df_customers").to_df())

# %%
customer_name = "Alice"
result = get_customer_orders(customer_name)
print(result)
