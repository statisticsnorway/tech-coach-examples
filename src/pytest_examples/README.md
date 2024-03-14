# Testing med pytest

## Hvordan kjøre pytest fra kommandolinjen?

For å kjøre pytest, kjør følgende kommando fra rotkatalogen i repoet:

```shell
poetry run pytest
```

For å kjøre pytest med beregning av testdekning for filene i pytest_examples
katalogen kjører du følgende kommando fra rotkatalogen i repoet:

```shell
poetry run pytest --cov=pytest_examples --cov-report term-missing
```
