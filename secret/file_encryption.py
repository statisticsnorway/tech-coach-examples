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
# # Kryptering av filer
# Noen ganger kan man ha behov for å kryptere mer enn noen enkelte passord, api-token
# eller hemmeligheter. Et eksempel kan være en konfig-fil som inneholder en rekke
# sensitive ting. Da kan det være lettere å kryptere hele filen, lese inn
# krypteringsnøkkelen fra miljøvariabel (`.env`-fil) og dekryptere når koden kjører.
#
# Denne filen viser et eksempel på dette.

# %%
import os
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet
from dapla import repo_root_dir
from dotenv import load_dotenv
from tomli import loads


# %% [markdown]
# ## Hjelpefunksjoner
# Verdt å merke seg i funksjonene nedenfor er at krypteringsbiblioteket bruker byte
# string som datatype og ikke vanlig string, mens miljøvariable leses inn som vanlig
# string type. Man kan konvertere mellom disse typene ved å bruke `decode()` og
# `encode()`, og det er grunnen til at det er en del bruk av dette i hjelpefunksjonene.


# %%
def generate_and_store_key(filename: Path = Path("mykey.key")) -> None:
    """Generate a key and save it to a file."""
    key = Fernet.generate_key()
    filename.write_text(key.decode())  # Write the key as a string, not bytes


# %%
def load_key_from_file(filename: Path = Path("mykey.key")) -> bytes:
    """Load a stored key from a file."""
    return filename.read_text().encode()


# %%
def load_key_from_env(key_id: str) -> bytes:
    """Load a key from an environment variable or .env file."""
    load_dotenv()
    key = os.getenv(key_id)
    if not key:
        raise ValueError(f"Environment variable {key_id} not found")
    return key.encode()


# %%
def encrypt_file(filename: Path, key: bytes) -> None:
    """Encrypt a file and store it with an .enc suffix."""
    f = Fernet(key)
    encrypted_data = f.encrypt(filename.read_bytes())
    encrypted_file = filename.with_name(f"{filename.name}.enc")
    encrypted_file.write_bytes(encrypted_data)


# %%
def decrypt_file(encrypted_file: Path, key: bytes) -> None:
    """Decrypt a file and store it without .enc suffix."""
    f = Fernet(key)
    encrypted_data = encrypted_file.read_bytes()
    decrypted_data = f.decrypt(encrypted_data)
    decrypted_file = encrypted_file.with_name(encrypted_file.stem)
    decrypted_file.write_bytes(decrypted_data)


# %%
def load_encrypted_config(encrypted_file: Path, key: bytes) -> dict[str, Any]:
    """Decrypt the file and return the decrypted config."""
    f = Fernet(key)
    encrypted_data = encrypted_file.read_bytes()
    decrypted_data = f.decrypt(encrypted_data)
    return loads(decrypted_data.decode())


# %% [markdown]
# ## Krypter og dekrypter tenkt sensitiv konfig-fil
# La oss si at filen `config/config.toml` i dette repoet er sensitiv og vi ønsker
# å kryptere den. Da må vi først lage en krypteringsnøkkel og legge den inn i en
# `.env`-fil.

# %%
generate_and_store_key()  # Create key and store in mykey.key

# %% [markdown]
# Funksjonen `generate_and_store_key()` lager en nøkkel og lagrer den i fila mykey.key.
# Åpne filen mykey.key og kopier verdien.
# Opprett en `.env`-fil i rotkatalogen på repoet, hvis du ikke har denne fila fra før.
# Legg til en linje i filen tilsvarende det nedenfor, men bytt ut verdien med den
# verdien du kopierte.
#
# `DECRYPT_KEY=a5kAMIGJFa-kehjKjYEu_dfKTe1yercjCeY-_ULzoT8=`
#
# Deretter laster vi inn nøkkelen og krypterer fila. Den krypterte fila blir lagret
# i samme katalog som den opprinnelige fila med endingen `.enc` lagt til filnavnet.
#
# **NB!** Det er veldig viktig å ta godt vare på krypteringsnøkkelen. Lagre den gjerne
# i en passordhåndterer eller et annet sikkert sted. Uten den får du ikke dekryptert
# filene.

# %%
key = load_key_from_env("DECRYPT_KEY")
config_file = repo_root_dir() / "config" / "config.toml"
encrypt_file(config_file, key)

# %% [markdown]
# Nå er fila kryptert. Legg til den krypterte fila i git og fjern den ukryptert fila
# fra git.
#
# Nå er alt klart til å lese konfig fra den krypterte fila.

# %%
config_file_encrypted = repo_root_dir() / "config" / "config.toml.enc"
config = load_encrypted_config(config_file_encrypted, key)
print(config)
