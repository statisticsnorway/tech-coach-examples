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
# # Jupytext
# [Jupytext](https://github.com/mwouts/jupytext)
# brukes for å kunne lagre Jupyter notebooks som rene pythonfiler, det vil si med
# ending `.py` i stedet for `.ipynb`. Rene pythonfiler gir en rekke
# fordeler med tanke på versjonskontroll og verktøy for kodekvalitetssjekk, og man
# slipper også stripping av output. Du kan fortsatt jobbe med filene som notebooks
# på vanlig måte.
#
# For å åpne en slik python-fil som Notebook i JupyterLab, høyreklikk på fila og velg
# Open With &rarr; Notebook.

# %% [markdown]
# ## Oppsett
# Det anbefales å konfigurere jupytext slik som det gjort i fila [pyproject.toml] i
# dette repoet, linje 41-44. Der bruker man prosent-formatet, noe som gir god støtte
# i VSCode, PyCharm og andre editorer. Oppsettet stripper også bort unødvendige metadata,
# slik at man slipper unødvendige oppdateringer og potensielle mergekonflikter. Oppsettet
# sørger også for at verktøyet [isort] virker riktig med filene.
#
# [pyproject.toml]: https://github.com/statisticsnorway/tech-coach-examples/blob/main/pyproject.toml
# [isort]: https://pycqa.github.io/isort/

# %% [markdown]
# En jupytext pythonfil ser typisk ut som dette i en vanlig editor:
# ```
# # ---
# # jupyter:
# #   jupytext:
# #     text_representation:
# #       extension: .py
# #       format_name: percent
# #       format_version: '1.3'
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
# ## Bruk av JupyterLab til å konvertere eksistrende .ipynb filer til jupytext .py
# Sørg for at oppsettet ovenfor er konfigurert i repoets `pyproject.toml` før du
# konverterer filer.
#
# Åpne hver .ipynb-fil på vanlig måte og lagre den på nytt.
# Da vil det i tillegg til .ipynb-filen bli opprettet en .py-fil med samme navn.
# Det er .py-filen som skal legges inn i git.
# Alle endringer du gjør i ipynb-filen blir automatisk speilet til py-filen, og motsatt.

# %% [markdown]
# ## Manuell konvertering av eksistrende .ipynb filer til jupytext .py
# Sørg for at oppsettet ovenfor er konfigurert i repoets `pyproject.toml` før du
# konverterer filer.
#
# Hvis du har Jypyter notebook filer i .ipynb-format og som du vil konvertere til
# .py-format for bruk med jupytext, kjører du følgende kommando:
# ```shell
# # convert notebook.ipynb to a .py file file in the double percent format
# jupytext --to py:percent notebook.ipynb
# ```
#
# Eller hvis du vil konvertere motsatt vei, så kjører du denne kommandoen:
# ```shell
# # convert notebook.py file to notebook.ipynb
# jupytext --to notebook notebook.py
# ```

# %% [markdown]
# ## Opprette nye filer jupytext .py filer
# Pass på at [pyproject.toml] inneholder  konfigurasjonen beskrevet ovenfor.
# Opprett en ny fil ved å åpne en ny notebook (File &rarr; New notebook) på vanlig måte.
# Da vil det i tillegg til .ipynb-filen bli opprettet en .py-fil med samme navn.
# Det er .py-filen som skal legges inn i git.
#
# Alle endringer du gjør i ipynb-filen blir automatisk speilet til py-filen, og motsatt.
#
# [pyproject.toml]: https://github.com/statisticsnorway/tech-coach-examples/blob/main/pyproject.toml

# %% [markdown]
# ## Eksempel på kodeceller

# %%
print("Hello world")
