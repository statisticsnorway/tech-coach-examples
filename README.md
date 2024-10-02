# tech-coach-examples

Dette repoet brukes av seksjon IT-Partner til å vise eksempler på kode og oppsett
for utvikling på Dapla.

## Katalogstruktur og eksempler

- _src_: Katalog for source kode
  - _automation:_ Katalog relatert til å kjøre mange ting i sekvens, dvs. autmatisering.
    - _papermill:_ Viser bruk og oppsett av [papermill].
    - _pythonfunctions:_ Anbefalt løsning. Se beskrivelse på [Confluence].
  - _jupyter:_ Katalog for jupyter notebooks eksempler
    - _jupytext_ipynb.py:_ Viser bruk og oppsett av [jupytext]
      for å lagre Jupyter notebooks som rene python-filer.
  - _logging:_ Eksempler på bruk av python logging. Se egen
     [README-fil](./src/logging/README.md) for detaljer.
  - _parquet:_ Eksempler som viser bruk av [parquet-filer], både fra pandas og fra
    duckdb. Se egen [README-fil](./src/parquet/README.md) for dette.
  - _pytest_examples_: Eksempel på kode som testes med pytest.
  - _secret:_ Eksempler som viser håndtering av hemmeligheter og kryptering
    av filer.
- _tests_: Katalog for tester (pytest)

[jupytext]: https://github.com/mwouts/jupytext#readme
[papermill]: https://papermill.readthedocs.io/en/latest/
[parquet-filer]: https://www.databricks.com/glossary/what-is-parquet
[pytest]: https://docs.pytest.org/
[confluence]: https://statistics-norway.atlassian.net/wiki/spaces/KOD/pages/3925147685/Hvordan+automatisere+Jupyter+notebooks+ved+bruk+av+funksjoner

## Hvordan installere og kjøre eksemplene?

```shell
poetry install --no-root
poetry run pytest -v --cov --cov-report=term-missing
```
