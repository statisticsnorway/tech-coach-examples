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
# # Papermill example
# Papermill can be used to run multiple notebooks in sequence. This example uses
# a parent file which runs the child files in sequence.
#
# ## Papermill and jupytext
# Papermill works on `*.ipynb`-files. If you are using jupytext to store the notebooks
# as plain `*.py`-files, and you don't have a corresponding paired `*.ipynb`-file, you
# need to create the child ipynb-files first. Do that using this command:
#
# `poetry run jupytext papermill_child*.py --to ipynb`
#
# ## Code

# %%
import dapla as dp
import pandas as pd
import papermill as pm


# %%
bucket = "gs://ssb-prod-tech-coach-data-produkt"
inndata_file = "ufo/inndata/valuta_p2020_p2023-09-21_v1.parquet"
inndata_path = f"{bucket}/{inndata_file}"
print(inndata_path)

process_step1_file = "temp/process_step1.parquet"
process_step1_path = f"{bucket}/{process_step1_file}"
print(process_step1_path)

klargjort_file = "ufo/klargjorte-data/valuta_monthly_p2022_v1.parquet"
klargjort_path = f"{bucket}/{klargjort_file}"
print(klargjort_path)

# %%
result = pm.execute_notebook(
    "papermill_child1.ipynb",
    "papermill_child1_output.ipynb",
    parameters=dict(in_path=inndata_path, out_path=process_step1_path),
)

# %%
result = pm.execute_notebook(
    "papermill_child2.ipynb",
    "papermill_child2_output.ipynb",
    parameters=dict(in_path=process_step1_path, out_path=klargjort_path),
)

# %%
print("Finished")
