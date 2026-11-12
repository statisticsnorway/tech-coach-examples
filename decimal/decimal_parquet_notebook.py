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
# # Desimaltall i Parquet-filer: Decimal vs Float
#
# Dette eksemplet demonstrerer hvorfor `Decimal` bør brukes fremfor `float` (`float64` / `DOUBLE`) når eksakte desimalverdier og korrekt avrunding er viktig, samt hvordan `Decimal`-kolonner lagres i Parquet-filer med logiske og fysiske datatyper.
#
# Vi vil også se på et ekstremt eksempel (`belop`-eksemplet) der store tall overskrider presisjonsgrensen for flyttall ($2^{53}$), og hvordan `Decimal` løser dette problemet.
#
# ## Forutsetninger
# Vi bruker `pandas` og `pyarrow` for å lese, skrive og analysere Parquet-dataene.

# %%
from decimal import ROUND_HALF_UP
from decimal import Decimal
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# %% [markdown]
# ## 1. Flyttall (`float64`) vs `Decimal`
#
# Standard flyttall følger IEEE 754-standarden og lagres i base 2. Dette betyr at desimaltall (base 10) som `103.55` ikke kan representeres helt nøyaktig.
#
# La oss se hva som skjer når vi formaterer `103.55` til mange desimaler, og hvordan avrunding påvirkes.

# %%
float_val = 103.55
decimal_val = Decimal("103.55")

print("=== Nøyaktig representasjon i minnet ===")
print(f"Float 103.55 med 50 desimaler:   {float_val:.50f}")
print(f"Decimal('103.55') eksakt verdi:  {decimal_val}")
print()

print("=== Avrunding til én desimal ===")
# Siden den underliggende flyttallsverdien er litt mindre enn 103.55 (103.549999...),
# vil round(103.55, 1) runde NED til 103.5 i stedet for OPP til 103.6.
print(f"Python round(103.55, 1):                 {round(float_val, 1)}")
print(
    f"Decimal ROUND_HALF_UP (avrunding):      {decimal_val.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)}"
)

# %% [markdown]
# ## 2. Store beløp og grensen for flyttalls-presisjon ($2^{53}$)
#
# En spesiell utfordring med flyttall oppstår når tallene blir svært store (f.eks. i nasjonalregnskap eller store finansielle transaksjoner).
# Grensen for nøyaktig heltallsrepresentasjon i `float64` er nøyaktig $2^{53} = 9007199254740992$.
#
# Over denne grensen kan ikke flyttall representere partalls/oddetalls-forskjeller nøyaktig, og de mister helt evnen til å lagre desimaler (f.eks. cent eller øre).
#
# La oss se på verdiene:
# * `9007199254740992.01`
# * `9007199254740992.02`

# %%
float_large_1 = float("9007199254740992.01")
float_large_2 = float("9007199254740992.02")

decimal_large_1 = Decimal("9007199254740992.01")
decimal_large_2 = Decimal("9007199254740992.02")

print("=== Store verdier med float64 vs Decimal ===")
print(f"Float 1:   {float_large_1}")
print(f"Float 2:   {float_large_2}")
print(f"Er de to flyttallene like?  {float_large_1 == float_large_2}")
print()
print(f"Decimal 1: {decimal_large_1}")
print(f"Decimal 2: {decimal_large_2}")
print(f"Er de to desimaltallene like? {decimal_large_1 == decimal_large_2}")

# %% [markdown]
# ## 3. Opprette og lagre testdata til Parquet
#
# Nå lager vi et test-datasett med ulike desimaltyper. Vi lagrer datasettet på to måter:
# 1. **Standard Decimal-lagring** (lagres som `FIXED_LEN_BYTE_ARRAY` i Parquet).
# 2. **Kompakt Decimal-lagring** (`store_decimal_as_integer=True`), som bruker standard heltallstyper (`INT32` / `INT64`) for desimaler med presisjon $\le 18$.

# %%
raw_values = ["103.55", "10.05", "1.15", "2.55", "1999.95"]

df = pd.DataFrame(
    {
        "item_id": pd.Series([1, 2, 3, 4, 5], dtype="int64[pyarrow]"),
        "amount_float64": pd.Series([float(v) for v in raw_values], dtype="float64"),
        # Python Decimal-objekter (PyArrow utleder automatisk som decimal128)
        "amount_py_decimal": [Decimal(v) for v in raw_values],
        # Eksplisitt PyArrow decimal128 med presisjon=8, skala=2
        "amount_decimal_p8": pd.Series(
            [Decimal(v) for v in raw_values],
            dtype=pd.ArrowDtype(pa.decimal128(8, 2)),
        ),
        # Eksplisitt PyArrow decimal128 med presisjon=15, skala=2
        "amount_decimal_p15": pd.Series(
            [Decimal(v) for v in raw_values],
            dtype=pd.ArrowDtype(pa.decimal128(15, 2)),
        ),
        # Eksplisitt PyArrow decimal128 med presisjon=25, skala=2
        "amount_decimal_p25": pd.Series(
            [Decimal(v) for v in raw_values],
            dtype=pd.ArrowDtype(pa.decimal128(25, 2)),
        ),
        # Eksplisitt PyArrow decimal128 med presisjon=18, skala=2 (inkluderer store testverdier)
        "belop": pd.Series(
            [
                Decimal("9007199254740992.01"),
                Decimal("9007199254740992.02"),
                None,
                None,
                None,
            ],
            dtype=pd.ArrowDtype(pa.decimal128(18, 2)),
        ),
    }
)

# Definer stier til testfiler (sjekker om vi kjører fra rotkatalogen eller fra decimal-mappen)
base_dir = Path("decimal") if Path("decimal").is_dir() else Path(".")
default_parquet = base_dir / "decimal_example.parquet"
int_parquet = base_dir / "decimal_as_int_example.parquet"

# Lagre begge versjoner
df.to_parquet(
    default_parquet, engine="pyarrow", index=False, store_decimal_as_integer=False
)
df.to_parquet(int_parquet, engine="pyarrow", index=False, store_decimal_as_integer=True)

print("Parquet-filer opprettet suksessfullt!")

# %% [markdown]
# ## 4. Inspisere Logiske og Fysiske datatyper i Parquet
#
# For en vanlig Parquet-leser eller visningsverktøy ser skjemaene helt like ut. Dette er fordi begge filene har de samme **logiske typene** (f.eks. `Decimal(18, 2)`).
#
# Men under panseret bruker de forskjellige **fysiske lagringstyper**. Vi kan bruke PyArrow til å inspisere dette direkte.


# %%
def show_parquet_column_types(parquet_path: Path) -> pd.DataFrame:
    parquet_file = pq.ParquetFile(parquet_path)
    pq_schema = parquet_file.schema
    arrow_schema = parquet_file.schema_arrow

    rows = []
    for i, col_schema in enumerate(pq_schema):
        arrow_field = arrow_schema.field(i)
        rows.append(
            {
                "column": col_schema.name,
                "physical_type": col_schema.physical_type,
                "logical_type": str(col_schema.logical_type),
                "arrow_type": str(arrow_field.type),
                "precision": col_schema.precision,
                "scale": col_schema.scale,
                "type_length": col_schema.length,
            }
        )
    return pd.DataFrame(rows)


# %%
print("=== Fysiske vs Logiske typer i decimal_example.parquet ===")
show_parquet_column_types(default_parquet)

# %%
print("=== Fysiske vs Logiske typer i decimal_as_int_example.parquet ===")
show_parquet_column_types(int_parquet)

# %% [markdown]
# ### Hva skjedde med `belop`?
# * I **`decimal_example.parquet`** lagres `belop` som en byte-array (`FIXED_LEN_BYTE_ARRAY` med lengde `8` bytes).
# * I **`decimal_as_int_example.parquet`** lagres `belop` som et standard heltal `INT64` (og lengden er `0` fordi bit-bredden er implisitt). Dette sparer lagringsplass og gir raskere lesing/skriving!

# %% [markdown]
# ## 5. Lese data tilbake til Pandas
#
# Vi kan enkelt lese filene tilbake til Pandas. Ved å bruke `dtype_backend="pyarrow"` sørger vi for at desimal-kolonnene beholdes som eksakte PyArrow-desimaler, i stedet for å konverteres til vanlige Python floats.

# %%
df_read = pd.read_parquet(default_parquet, engine="pyarrow", dtype_backend="pyarrow")
df_read

# %%
print("DataFrame dtypes:")
print(df_read.dtypes)
