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

# %% [markdown]
# # Lagring av testdata til fil for bruk ved testing
# Denne notebooken viser hvordan man enkelt kan lagre det som går inn og ut av en
# funksjon til fil, og som senere kan brukes ved testing.
#
# Dette kan være en enkel og kjapp måte å komme i gang med å teste en funksjon, der hvor
# det kan være litt komplekst å bygge opp input-data og fasit manuelt.
# Et eksempel kan være en funksjon som tar inn en eller flere dataframes og returner
# en dataframe.
#
# Eksemplet her illustrerer en notebook som kaller en funksjon, typisk slik det gjøres
# i et produksjonsløp. Sett `write_test_data = True` og kjør notebooken på vanlig måte.
# Da lagres input-dataframe og fasit-dataframe til fil, og som du senere kan bruke
# ved testing.

# %%
import dapla as dp
import pandas as pd


write_test_data = True


# %%
# The function to test
def add_column_sum(df: pd.DataFrame) -> pd.DataFrame:
    """Adds a new column 'C' to the DataFrame, which is the sum of columns 'A' and 'B'.

    Args:
        df: The input DataFrame

    Returns:
        The modified DataFrame with the new column 'C'
    """
    df["C"] = df["A"] + df["B"]
    return df


# %%
# Create a sample dataset
df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df

# %%
result = add_column_sum(df)
result.head()

# %%
in_file = dp.git.repo_root_dir() / "tests" / "testdata" / "dataset1.parquet"
facit_file = dp.git.repo_root_dir() / "tests" / "testdata" / "facit1.parquet"

# %%
if write_test_data:
    df.to_parquet(in_file)
    result.to_parquet(facit_file)
