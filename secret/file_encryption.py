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

# %%
from cryptography.fernet import Fernet
from pathlib import Path
from dapla import repo_root_dir


# %% [markdown]
# ## Hjelpefunksjoner

# %%
def generate_and_store_key(filename: Path = Path("mykey.key")) -> None:
    """Generates a key and save it into a file."""
    key = Fernet.generate_key()
    filename.write_text(key.decode())  # Write the key as a string, not bytes


# %%
def load_key_from_file(filename: Path = Path("mykey.key")) -> bytes:
    """Loads the key from the current directory"""
    return filename.read_text().encode()


# %%
def encrypt_file(filename: Path, key: bytes) -> None:
    """Encrypt a file and store it with an .enc suffix."""
    f = Fernet(key)
    encrypted_data = f.encrypt(filename.read_bytes())
    encrypted_file = filename.with_name(filename.name + ".enc")
    encrypted_file.write_bytes(encrypted_data)


# %%
def decrypt_file(encrypted_file: Path, key: bytes) -> None:
    """Encrypt a file and store it with an .enc suffix."""
    f = Fernet(key)
    encrypted_data = encrypted_file.read_bytes()
    decrypted_data = f.decrypt(encrypted_data)
    decrypted_file = encrypted_file.with_name(encrypted_file.stem)
    decrypted_file.write_bytes(decrypted_data)


# %% [markdown]
# ## Krypter og dekrypter tenkt sensitiv konfig-fil
# TBD

# %%
generate_and_store_key()
key = load_key_from_file()

config_file = repo_root_dir() / "config" / "config.toml"
encrypt_file(config_file, key)
# %%
