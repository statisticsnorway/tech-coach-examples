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
from fagfunksjoner.paths.project_root import ProjectRoot


with ProjectRoot():
    from config_examples.ConfigReader import ConfigReader

# %%
config = ConfigReader()

print(config.config["paths"]["inndata_dir"])


# %%
directory = config.klargjort_dir()
print(directory)
