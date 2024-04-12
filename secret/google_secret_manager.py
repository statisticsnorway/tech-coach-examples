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
# This file is a Jupyter Notebook stored in plain text format as a .py file.
# Open as notebook in Jupyter by right-clicking the file and select
# Open With -> Notebook.

# %% [markdown]
# # Google Secret Manager
# ## Bruk av .env fil
# Standard måte å håndtere hemmeligheter i kode på er å skjule dem i miljøvariabler
# som leses inn fra en `.env` fil. Dette er beskrevet på
# https://statistics-norway.atlassian.net/wiki/spaces/BEST/pages/3216703491/Hvordan+h+ndtere+hemmeligheter+og+passord+i+git
#
# Dette virker, men det kan være en utfordring å distribuere endringer av
# hemmelighetene i teamet. Hvor skal de lagres, og hvordan skal de sendes til de andre
# i teamet ved oppdateringer?
#
# Google Secret Manager er et godt alternativ for dette.
#
# ### Verdt å merke seg
# Du må fortsatt bruke `.env`-fil, for noen av de parametrene du trenger for å hente ut
# hemmeligheter fra Google Secret Manager anses også som hemmeligheter. Men det du
# vinner er at parametrene er statiske, slik at ikke trenger å distribuere noe i teamet
# når hemmelightene oppdateres.
#
# ## Kodeeksempler


# %%
import os

from dapla import AuthClient
from dotenv import load_dotenv
from google.api_core.exceptions import NotFound
from google.cloud import secretmanager
from google.cloud.secretmanager_v1.types import Replication, Secret


# %%
load_dotenv()  # Laster inn .env fil og setter miljøvariable
project_id = os.getenv("TECH_COACH_DEV_GCP_PROJECT_ID")
print(project_id)

# %% [markdown]
# ## Bruk av Google Secret Manager
# Google Secret Manager er per nå ikke tilgjengelig for standard Dapla-team. Behovet for
# en god måte å håndtere og distribuere hemmeligheter på er meldt til produkteier Dapla,
# og enten blir det en tjeneste på Dapla eller som minimum at blir en feature som kan
# enables.
#
# Koden nedenfor tar utgangspunkt i et GCP-prosjekt hvor Google Secret Manager er enablet.
#
# ### Verdt å tenke på
#
# For å hente ut en hemmelighet fra Google Secret Manager så trenger man GCP projekt ID
# og en secret_id, navnet på hemmeligheten, man skal hente.
#
# Per nå er GCP projekt ID definert til å håndteres som en hemmelighet, det vil si leses
# inn fra .env-fil. Man NAV behandler den ikke som hemmelig, så det er mulig at det blir
# en endring på det.
#
# Secret_id kan være sensitiv hvis man navngir den med et beskrivende navn, for eksempel
# SSB_ORACLE_MASTER_PASSWORD, men trenger ikke være det hvis man navngir den mer anonymt,
# for eksempel SECRET1. Så i en del tilfeller kan secret_id også måtte leses fra .env-fil.
#
# Så det man vinner på å bruke Google Secret Manager er først og fremst at man slipper
# å distribuere endringer. Dette siden secret_id og GCP prosjekt id er statiske.
#
# ### Opprett hemmelighet

# %%
# ID of the secret to create.
secret_id = "YOUR_SECRET_ID1"

base_name = f"projects/{project_id}"
secret_name = f"{base_name}/secrets/{secret_id}"
version_name = f"{secret_name}/versions/latest"

# Create the Secret Manager client.
credentials = AuthClient.fetch_google_credentials()
client = secretmanager.SecretManagerServiceClient(credentials=credentials)

replication_policy = Replication(
    user_managed=Replication.UserManaged(
        replicas=[Replication.UserManaged.Replica(location="europe-north1")]
    )
)

try:
    # Attempt to access the secret
    secret = client.access_secret_version(request={"name": version_name})
    versions = client.list_secret_versions(request={"parent": secret_name})
    for version in versions:
        print(f"Version: {version.name}, State: {version.state.name}")
    print(f"Secret {secret_id} already exist, create a new version of the secret.")
except NotFound:
    # If not found, create a new secret
    secret = client.create_secret(
        request={
            "parent": base_name,
            "secret_id": secret_id,
            "secret": Secret(replication=replication_policy),
        }
    )
    print(f"New secret {secret_id} created")

# Add the secret version.
version = client.add_secret_version(
    request={"parent": secret_name, "payload": {"data": b"hello world!"}}
)

# %% [markdown]
# ## Les hemmelighet

# %%
# Access the secret version
response = client.access_secret_version(request={"name": version_name})

# Print the secret payload.
payload = response.payload.data.decode("UTF-8")
print(f"Secret {response.name} payload: {payload}")
