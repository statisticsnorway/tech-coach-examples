# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
# ---

# %% [markdown]
# # Jupytext
# [Jupytext](https://github.com/mwouts/jupytext)
# brukes for å kunne lagre Jupyter notebooks som rene python filer. Det gir en rekke
# fordeler med tanke på versjonskontroll og verktøy for kodekvalitetssjekk, og man
# slipper også stripping av output.
#
# For å åpne en slik python-fil i JupyterLab, høyreklikk på fila og velg
# Open With &rarr; Notebook.

# %% [markdown]
# ## Oppsett
# Det anbefales å konfigurere jupytext slik som det gjort i fila `pyproject.toml` i
# dette repoet, linje 34-45. Der bruker man prosent-formatet, noe som gir god støtte
# i VSCode, PyCharm og andre editorer. Oppsettet stripper også bort unødvendige metadata,
# slik at man slipper unødvendige oppdateringer og potensielle mergekonflikter.

# %% [markdown]
# En slik jupytext python-fil ser typisk ut som dette i en vanlig editor:
# ```
# # ---
# # jupyter:
# #   jupytext:
# #     text_representation:
# #       extension: .py
# #       format_name: light
# #       format_version: '1.5'
# # ---
#
# # %% [markdown]
# # # Jupytext
#
# # %%
# import os
# print("Hello world")
# ```

# %% [markdown]
# ## Konvertere filer fra .ipynb til .py
# Hvis du har Jypyter notebook filer i .ipynb-format og som du vil konvertere til
# .py-format for bruk med jupytext, kjører du følgende kommando:
# ```shell
# # convert notebook.ipynb to a .py file file in the double percent format
# jupytext --to py:percent notebook.ipynb
# ```
#
# Eller hvis du vil konvertere motsatt vei, så kjører du denne kommandoen:
# ```shell
# # convert .py file to notebook.ipynb
# jupytext --to notebook notebook.py
# ```

# %% [markdown]
# ## Eksempel på kodeceller

# %%
import os


print("Hello world")

# %%
print("New Cell")
