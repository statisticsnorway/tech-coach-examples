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

# %% tags=["parameters"]
# Tagged with "parameters" in jupyter
in_path = ""
out_path = ""

# %%
print(f"{in_path=}")
print(f"{out_path=}")

# %%
import dapla as dp
import pandas as pd


# %%
df = dp.read_pandas(gcs_path=in_path)
df

# %%
# Calculate mean per month for each currency
df2 = df.pivot_table(index="TIME_PERIOD", columns="BASE_CUR")
df3 = df2.groupby(pd.Grouper(freq="M")).mean()
df3

# %%
dp.write_pandas(df3, out_path)
print(f"Wrote dataset to {out_path}")
