# Decimal i Parquet-filer (Pandas og PyArrow)

Dette eksemplet viser hvorfor `Decimal` bør brukes fremfor `float` (`float64` / `DOUBLE`) når eksakte desimalverdier og korrekt avrunding er viktig, samt hvordan `Decimal`-kolonner lagres i Parquet-filer med logiske og fysiske datatyper.

## Hvorfor `Decimal` fremfor `float`?

Flyttall (`float` i Python / `float64` i Pandas / `DOUBLE` i Parquet) følger IEEE 754-standarden og representerer tall som binære brøker (base 2). Mange vanlige desimaltall i base 10 kan **ikke** representeres eksakt binært.

Et klassisk eksempel er **`103.55`**:
- I `float64` lagres `103.55` egentlig som:
  `103.5499999999999971578290569595992565155029296875`
- Fordi den binære verdien er ørlite mindre enn `103.55`, vil avrunding til én desimal (`round(103.55, 1)`) runde **ned** til `103.5` i stedet for **opp** til `103.6` (selv om man ved vanlig avrunding `ROUND_HALF_UP` ønsker `103.6`).
- Ved beregninger og sammenligninger oppstår avrundingsfeil (f.eks. gir `103.55 + 0.1` verdien `103.64999999999999` og `103.55 * 3` gir `310.65000000000003`).

Med `Decimal` (og `pa.decimal128(precision, scale)` i PyArrow/Parquet) lagres `103.55` eksakt som heltallet `10355` med skala `2` ($10355 \times 10^{-2}$).

## Logisk og fysisk type i Parquet

Parquet skiller mellom:
- **Logisk type (`logical_type`)**: Hvordan dataene skal tolkes semantisk, f.eks. `Decimal(precision=15, scale=2)`.
- **Fysisk type (`physical_type`)**: Hvordan bytene faktisk lagres på disk i Parquet-fila:
  - `float64` lagres med fysisk type `DOUBLE` og logisk type `None`.
  - `Decimal` lagres som standard i PyArrow med fysisk type `FIXED_LEN_BYTE_ARRAY` (der `type_length` er antall bytes som trengs for den angitte `precision`).
  - Hvis man angir `store_decimal_as_integer=True` ved skriving til Parquet, bruker PyArrow mer kompakte heltallstyper når `precision <= 18`:
    - `1 <= precision <= 9`: Fysisk type `INT32`
    - `10 <= precision <= 18`: Fysisk type `INT64`
    - `precision >= 19`: Fysisk type `FIXED_LEN_BYTE_ARRAY`

## Kjøre eksemplet

Fra rotkatalogen i repoet:

```shell
poetry run python decimal/decimal_parquet_example.py
```

For å verifisere at Parquet-filene også leses med eksakte `Decimal`-verdier i R (med `arrow`-pakken):

```shell
Rscript decimal/verify_decimal_parquet.R
```
