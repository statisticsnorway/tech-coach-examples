#!/usr/bin/env python3
"""
Eksempel: Les samme TOML-fil både med tomllib og Dynaconf
"""
import tomllib
from pathlib import Path
from dynaconf import Dynaconf

# Absolutt sti til TOML-filen
CONFIG_PATH = Path("/buckets/produkt/tech-coach-examples/konfigurasjon/env/firmakonfig_v1.toml")

def read_with_tomllib(path: Path):
    """Les filen med tomllib"""
    if not path.exists():
        raise FileNotFoundError(f"Finner ikke {path}")

    with path.open("rb") as f:
        data = tomllib.load(f)

    firmainfo = data.get("konfig", {}).get("firmainfo", {})
    print("\n--- TOMLLIB ---")
    for key, section in firmainfo.items():
        navn = section.get("firmanavn", "<ukjent>")
        orgnr = section.get("orgnummer", "<ukjent>")
        print(f"{key}: {navn} (Org.nr: {orgnr})")


def read_with_dynaconf(path: Path):
    """Les filen med Dynaconf"""
    settings = Dynaconf(
        settings_files=[str(path)],
        environments=False,
    )
    print("\n--- DYNACONF ---")
    for key, section in settings.konfig.firmainfo.items():
        print(f"{key}: {section.firmanavn} (Org.nr: {section.orgnummer})")


if __name__ == "__main__":
    print(f"Bruker konfig-fil: {CONFIG_PATH}")
    read_with_tomllib(CONFIG_PATH)
    read_with_dynaconf(CONFIG_PATH)
