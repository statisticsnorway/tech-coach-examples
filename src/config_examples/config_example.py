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
from config.config import settings


# %%
print(f"{settings.dapla_team=}")
print(f"{settings.short_name=}")
print(f"{settings.kildedata_root_dir=}")
print(f"{settings.product_root_dir=}")
print(f"{settings.inndata_dir=}")
print(f"{settings.klargjort_dir=}")
print(f"{settings.statistikk_dir=}")
print(f"{settings.utdata_dir=}")

# %%
weather_stations_file = f"{settings.inndata_dir}/frost/weather_stations_v1.parquet"
print(weather_stations_file)
