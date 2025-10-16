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
# # Hvordan se på csv-filer med Excel-lignenede funksjonalitet

# %%
from pathlib import Path

import pandas as pd
from dapla import repo_root_dir
from ipydatagrid import DataGrid
from IPython.display import display


# %%
# Erstatt katalog og filnavn med dine data
directory = Path(repo_root_dir()) / "src" / "parquet" / "dataset"
filename = "customers.csv"

# %%
df = pd.read_csv(directory / filename)
print(df.head())

grid = DataGrid(df)
display(grid)
