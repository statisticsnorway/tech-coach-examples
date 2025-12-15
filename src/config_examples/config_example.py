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
# # Bruk av Config-filer
# Denne filen viser bruk av config-filer. Config-filene er lagret i `.toml`-format i
# katalogen `config`, og vi bruker biblioteket [DynaConf](https://www.dynaconf.com/)
# til å lese inn filene.


# %%
from config.config import settings
from config.config import settings_simple


# %% [markdown]
# ## Standard oppsett
# Med dette oppsettet slipper du å endre mange steder når du bytter for eksempel
# produksjonsår eller bytter kjømiljø fra prod til test. Se filen `settings.toml`
# i config-katalogen.
#
# Ting som produksjonsår og kjøremiljø settes en gang, og så kan man gjenbruke det
# i de andre variablene man setter, via noe som kalles *string substitions*.
# Eksempel:
#
# DB_NAME = "mydb.db"
# DB_PATH = "@format /buckets/produkt/{this.DB_NAME}"

# %%
print(f"{settings.dapla_team=}")
print(f"{settings.short_name=}")
print(f"{settings.kildedata_root_dir=}")
print(f"{settings.product_root_dir=}")
print(f"{settings.inndata_dir=}")
print(f"{settings.klargjort_dir=}")
print(f"{settings.statistikk_dir=}")
print(f"{settings.utdata_dir=}")
print(f"{settings.temporary_run=}")

# %%
weather_stations_file = f"{settings.inndata_dir}/frost/weather_stations_v1.parquet"
print(weather_stations_file)

# %% [markdown]
# ## Enkelt oppsett
# Med dette oppsettet kan du ikke gjenbruk variable, så du må manuelt bytte ut alle
# steder hvor en variabel er brukt. Hvis du for eksempel bytter fra å kjøre i
# prod-miljøet til i test-miljøet, så må du gå gjennom alle bøttestier å endre `prod`
# til `test`. Men til gjengjeld er config-filene lettere å forstå siden den ikke bruker
# spesiell syntaks.


# %%
print(f"{settings_simple.dapla_team=}")
print(f"{settings_simple.short_name=}")
print(f"{settings_simple.directories.kildedata_root_dir=}")
print(f"{settings_simple.directories.product_root_dir=}")
print(f"{settings_simple.directories.inndata_dir=}")
print(f"{settings_simple.directories.klargjort_dir=}")
print(f"{settings_simple.directories.statistikk_dir=}")
print(f"{settings_simple.directories.utdata_dir=}")
