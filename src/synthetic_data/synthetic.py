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
import pandas as pd
from faker import Faker
from hack4ssb2025_faker import SSBFaker


# %% [markdown]
# # Enkelt bruk av standard faker
# Dette viser enkel bruk av standard faker til å generere norske navn, adresser osv.

# %%
fake = Faker("no_NO")
print(fake.name())
print(fake.address())
print(fake.phone_number())
print(fake.license_plate())


# %%
def generate_faker_df(rows: int) -> pd.DataFrame:
    fake = Faker("no_NO")
    data = []
    for _ in range(rows):
        data.append(
            {
                "name": fake.name(),
                "address": fake.street_address(),
                "phone": fake.phone_number(),
                "license-plate": fake.license_plate(),
            }
        )
    return pd.DataFrame(data)


# %%
df = generate_faker_df(10)
df.head()

# %% [markdown]
# # Bruk av hack4ssb2025-faker
# På hack4SSB i 2025 var det en gruppe som blant annet lagde nye faker-metoder for
# variabler som er mye brukt i SSB. For eksempel fødselsnummer, org-nummer osv.
# Her er eksempel på bruk av dette.
#
# For mange av variablene trekkes verdiene fra kodelister i klass.
#
# Biblioteket er ikke lagt ut på PyPI ennå, men det kan installeres med denne kommandoen:
# `poetry add git+https://github.com/statisticsnorway/hack4ssb2025-faker.git#main`.

# %%
ssb_fake = SSBFaker()
columns = [
    "fnr",
    "kommune",
    "fylke",
    "orgnr",
    "snr",
    "nace",
    "yrkeskode",
    "utdanning",
    "sivilstand",
    "landkode",
]
ssb_df = ssb_fake.create_data(columns, n=10)
ssb_df.head()
