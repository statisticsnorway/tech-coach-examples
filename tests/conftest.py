import pandas as pd
import pytest


@pytest.fixture
def multiindex() -> pd.DataFrame:
    # Define the multi-level index
    multi_index = pd.MultiIndex.from_tuples(
        [
            ("New York", "Store A"),
            ("New York", "Store B"),
            ("Los Angeles", "Store A"),
            ("Los Angeles", "Store B"),
            ("Chicago", "Store A"),
            ("Chicago", "Store B"),
        ],
        names=["City", "Store"],
    )
    data = {
        "Sales": [200, 240, 150, 300, 200, 100],
        "Customers": [30, 45, 20, 50, 25, 15],
    }
    df = pd.DataFrame(data, index=multi_index)
    df_reset = df.reset_index()
    return df_reset
