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
# # Bruk av Synthetic Data Vault (sdv)
# Denne filen viser bruk av [python-biblioteket sdv](https://github.com/sdv-dev/SDV)
# til generere syntetiske data. Det baserer seg på å analysere dine eksisterende data
# og så generere nye syntetiske data med lignende statistiske egenskaper. 

# %%
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import Metadata
import pandas as pd
from pathlib import Path

# %%
filename = "/buckets/produkt/metstat/inndata/frost/weather_stations_v2.parquet"
df = pd.read_parquet(filename)
df.head()

# %%
# Automatically infer metadata from the real data
metadata = Metadata.detect_from_dataframe(data=df, table_name="weather_stations")

metadata_file = Path("sdv_metadata.json")
metadata_file.unlink(missing_ok=True)  # Delete if exist

metadata.save_to_json("sdv_metadata.json")
print(metadata)

# %%
# Create and train synthesizer model (GaussianCopula is a good general-purpose model)
synthesizer = GaussianCopulaSynthesizer(metadata)
synthesizer.fit(df)

# %%
# Generate synthetic data
df_synthetic = synthesizer.sample(num_rows=len(df))
df_synthetic.head(200)

