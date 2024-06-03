from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


def generate_unique_numbers(low: int, high: int, size: int) -> list[int]:
    """Generates a list of unique random numbers within a specified range.

    Args:
        low: The lower bound of the range (inclusive).
        high: The upper bound of the range (exclusive).
        size: The number of unique random numbers to generate.

    Returns:
        A list of unique random numbers within the specified range.
    """
    seed = 0  # For initializing the random generator
    rng = np.random.default_rng(seed)
    numbers = set()
    while len(numbers) < size:
        numbers.add(rng.integers(low, high))
    return list(numbers)


def replace_org_info(
    df: pd.DataFrame, org_number_column: str, org_name_column: str | None = None
) -> pd.DataFrame:
    """Replace org numbers and names with new randomly generated values.

    Args:
        df: The dataframe containing org numbers and org names.
        org_number_column: The column containing organization numbers to be replaced.
        org_name_column: The column name containing organization names to be
            replaced (optional).

    Returns:
        A dataframe with org information replaced by new randomly generated values.
    """
    if org_number_column not in df.columns:
        raise ValueError(f"Column {org_number_column} not found in dataframe")

    # Generate new random org number with 9 digits
    unique_org_numbers = df[org_number_column].unique()
    new_numbers = generate_unique_numbers(100000000, 999999999, len(unique_org_numbers))

    number_mapping = dict(zip(unique_org_numbers, new_numbers, strict=False))
    df[org_number_column] = df[org_number_column].map(number_mapping)

    if org_name_column:
        if org_name_column not in df.columns:
            raise ValueError(f"Column {org_name_column} not found in dataframe")

        unique_org_names = df[org_name_column].unique()
        fake = Faker("no_NO")
        new_names = [fake.unique.company() for _ in range(len(unique_org_names))]
        name_mapping = dict(zip(unique_org_names, new_names, strict=False))
        df[org_name_column] = df[org_name_column].map(name_mapping)

    return df


if __name__ == "__main__":
    # Clean org numbers and names from in_file and store in out_file
    in_file = Path(__file__).parent / "testdata" / "valuta_omv_inndata.parquet"
    out_file = Path(__file__).parent / "testdata" / "cleaned_file.parquet"

    in_df = pd.read_parquet(in_file)
    clean_df = replace_org_info(in_df, "rapp_orgnr", "vof_navn")
    clean_df.to_parquet(out_file)
