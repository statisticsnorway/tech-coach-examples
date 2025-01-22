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

## Bruk av dynaconf til å lese konfig-filer

Vi anbefaler bruk av biblioteket [Dynaconf] til å lese og jobbe med konfig-filer i
python. Det støtter blant annet gjenbruk av variabler. Det vil si at man i en variabel
i konfig-filen kan gjenbruke andre variabler. Et eksempel på dette kan være at man
definerer et årstall og så gjenbrukes dette årstallet i et filnavn.
Dette gjøres ved hjelp av en `@format`-syntaks som vist i dette eksemplet:

```toml
year = "2024"
weather_data_file_name = "@format weather_data_p{this.year}.parquet"
```

Dynaconf bruker to filer som legges i en `config`-mappe:

- `settings.toml`: Selve konfigurasjonene
- `config.py`: Leser inn konfig-filen og gjør variablene tilgjengelig via et settings-objekt.

Dynaconf støtter også validering, bruk av miljøer med mer.
Se [tech-coach-stat repoet] for et eksempel på mer avansert bruk.

## Eksempel: Bruk av konfig-filer på DAPLA

Eksempelet vårt viser hvordan en .toml konfig-fil kan brukes på DAPLA

### Detaljer om filene i eksemplet

```shell
├── config
    ├── config.py
    └── settings.toml
├── src
    ├── config_examples
        ├── config_examples.py
        └── README.md
```

`config`-katalogen inneholder .toml-fil med konfigurasjonsvariabler og `config.py` som nevnt ovenfor.
`src/config_examples`-katalogen inneholder eksempel på bruk

`config_examples.py` viser hvordan du kan hente ut bruke konfigurasjonsvariablene i din egen kode.
`README.md`: Denne filen.

[Dynaconf]: https://www.dynaconf.com/
[tech-coach-stat repoet]: https://github.com/statisticsnorway/tech-coach-stat/tree/main/config
