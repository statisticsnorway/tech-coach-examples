# Eksempler på bruk av parquet-filer

## Hva er parquet-filer?

Parquet er et Open Source, kolonneorientert filformat som er laget for
effektiv håndtering av store store datamengder. Parquet er kompatibelt med de
fleste Bigdata plattformer og rammeverk. SSB har standardisert på parquet som
lagringsformat for ferdig prosesserte data i datatilstandene inndata,
klargjorte data og statistikkdata.

Se også [beskrivelse av parquet-formatet](https://www.databricks.com/glossary/what-is-parquet).

## Eksempel 1: Spørring på databaselignende tabeller

Vi har laget et eksempel hvor dataene ligger i parquet-filer tilsvarende tabeller i
en relasjonell database. Eksemplet har tabeller for kunder, produkter, ordre osv.
Tabellene og dataene er beskrevet i [dataset.md](dataset.md).

Oppgave: Hvilke produkter har Alice bestilt?

Fila `queries_pandas.py` viser hvordan dette gjøres med pandas, og fila
`queries_duckdb.py` viser hvordan det gjøres med duckdb (SQL).

### Hvordan kjøre eksemplet?

Kjør følgende kommandoer fra et terminalvindu:

```shell
git clone https://github.com/statisticsnorway/tech-coach-examples.git
cd tech-coach-examples/parquet
poetry install
poetry run python3 queries_pandas.py
poetry run python3 queries_duckdb.py
```

### Detaljer om filene i eksemplet

```shell
├── parquet
    ├── dataset
    │   ├── categories.csv
    │   ├── customers.csv
    │   ├── details.csv
    │   ├── orders.csv
    │   └── products.csv
    ├── dataset.md
    ├── dataset.py
    ├── queries_duckdb.py
    ├── queries_pandas.py
    └── README.md
```

`dataset`-katalogen inneholder csv-filer med data for hver tabell.

`dataset.py` inneholder en funksjon som lager parquet-filer fra csv-filene.
`dataset.md` beskriver datasettene og dataene.

`queries_duckdb.py` viser hvordan man spør på datasettene ved hjelp av duckdb.

`queries_pandas.py` viser hvordan man spør på datasettene ved hjelp av pandas.

`README.md`: Denne filen.
