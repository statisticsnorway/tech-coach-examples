from math import sqrt

import pandas as pd


def is_prime(number: int) -> bool:
    """Check if the given number is a prime number.

    Args:
        number: The number to check.

    Returns:
        True if the number is a prime number. False otherwise.
    """
    if not isinstance(number, int):
        raise TypeError("Number must be an integer.")
    if number <= 1:
        return False
    for i in range(2, int(sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True


# Function from fagfunksjoner.data.pandas_combinations
def flatten_col_multiindex(df: pd.DataFrame, sep="_") -> pd.DataFrame:
    """If the dataframe has a multiindex as a column.

    Flattens it by combining the names of the multiindex, using the seperator (sep).
    """
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [sep.join(col).strip().strip(sep) for col in df.columns.values]
    return df
