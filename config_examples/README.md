# Eksempel på bruk av konfig-filer

## Hva er konfig-filer i python?

Konfigurasjonsfiler i Python er vanligvis tekstfiler som inneholder innstillinger eller konfigurasjonsdata for en modul, program eller et prosjekt. Disse filene brukes til å lagre ulike variabler og andre konfigurasjonsparametere som kan endres og konfigurerer uten at selve koden må endres.

En vanlig type konfigurasjonsfil er TOML-filer (Tom's Obvious, Minimal Language). TOML er et enkelt filformat som er enkelt å lese og skrive, og det er populært blant Python-utviklere for konfigurasjonsformål. TOML-filer organiseres vanligvis i seksjoner, som hver inneholder nøkkel-verdi-par.

Her er et eksempel på en TOML-konfigurasjonsfil:

```shell
[server]
host = "localhost"
port = 8080

[database]
username = "admin"
password = "secret"
```

I dette eksemplet er det to seksjoner: [server] og [database]. Hver seksjon inneholder nøkkel-verdi-par som representerer forskjellige innstillinger eller konfigurasjonsdata.
For eksempel inneholder [server]-seksjonen tjener og portinnstillinger,
mens [database]-seksjonen inneholder brukernavn og passord for en database.

## Grunnleggende: Lesing av konfig-filer

For å lese og håndtere innholdet i en TOML-fil med Python, kan man for eksempel bruke biblioteket toml som kan
lese og skrive TOML-formatet. Et eksempel på bruk av toml-biblioteket for å lese en TOML-fil i Python kan være som følger:

```shell
import toml

with open("config.toml", "r") as f:
    config = toml.load(f)

print(config["server"]["host"])
print(config["database"]["username"])
```

Dette vil lese innholdet av config.toml-filen og lagre det som et Python-dictionary-objekt, som deretter kan brukes til å få tilgang til konfigurasjonsdataene i koden.

## Eksempel: Bruk av konfig-filer på DAPLA

Eksempelet vårt viser hvordan en .toml konfig-fil kan brukes på DAPLA

### Detaljer om filene i eksemplet

```shell
├── config
    ├── config.toml
├── config_examples
    ├── config_examples.py
    ├── ConfigReader.py
    └── README.md
```

`config`-katalogen inneholder en .toml-fil med konfigurasjonsvariabler.
`config_examples`-katalogen inneholder python filer for å behandle konfigurasjonsdataene fra .toml filen

`config.toml` inneholder konfigurasjonsvariabler brukt i dette eksempelet
`config_examples.py` leser konfigurasjonvariabler fra `config.toml` via `ConfigReader` og viser hvordan disse variablene kan nåes og benyttes med python.
`ConfigReader.md` definerer en klasse, kalt `ConfigReader`, som brukes til å lese konfigurasjonsfiler i TOML-format og gjør innholdet tilgjengelig via objektattributtet `self.config`.

`README.md`: Denne filen.
