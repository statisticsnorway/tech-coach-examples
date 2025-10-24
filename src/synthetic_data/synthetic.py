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
