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
from IPython.display import display


# %%
def read_data(in_path):
    print("child1.read_data")  # Should use logging, but simplify example by using print
    df = dp.read_pandas(gcs_path=in_path)
    display(df.head())
    return df


# %%
# Data minimizing, extract only the necessary columns.
def process_data(df):
    print("child1.process_data")
    df2 = df[["BASE_CUR", "TIME_PERIOD", "OBS_VALUE"]]
    return df2


# %%
def write_data(df, out_path):
    print("child1.write_data")
    display(df.head())
    dp.write_pandas(df, out_path)
    print(f"Wrote dataset to {out_path}")


# %%
def run_all(in_path, out_path):
    df = read_data(in_path)
    df2 = process_data(df)
    write_data(df2, out_path)


# %%
if __name__ == "__main__":
    in_path = "gs://ssb-prod-dapla-felles-data-delt/tech-coach/automation/valuta_p2020_p2023-09-21_v1.parquet"
    out_path = "gs://ssb-prod-dapla-felles-data-delt/tech-coach/automation/process_step1.parquet"
    print(f"{in_path=}")
    print(f"{out_path=}")

    run_all(in_path, out_path)
