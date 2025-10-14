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

# %% [markdown]
# from pathlib import Path
# from ipydatagrid import DataGrid
# from IPython.display import display
#
# import pandas as pd

# %%
# Erstatt katalog og filnavn med dine data
directory = Path.cwd() / "dataset"
filename = "customers.csv"

# %%
df = pd.read_csv(directory / filename)

grid = DataGrid(df)
display(grid)
