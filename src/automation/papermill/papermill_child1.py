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


# %%
df = dp.read_pandas(gcs_path=in_path)
df.head()

# %%
# Data minimizing, extract only the necessary columns.
df2 = df[["BASE_CUR", "TIME_PERIOD", "OBS_VALUE"]]
df2.head()

# %%
dp.write_pandas(df2, out_path)
print(f"Wrote dataset to {out_path}")
