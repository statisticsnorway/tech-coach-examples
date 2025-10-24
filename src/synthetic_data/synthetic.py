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
from faker import Faker
import pandas as pd

# %%
fake = Faker("no_NO")
print(fake.name())
print(fake.address())
print(fake.phone_number())
