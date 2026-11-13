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
# Vi vil også se på et eksempel (`belop`-eksemplet) der store tall overskrider presisjonsgrensen for flyttall (2^53), og hvordan `Decimal` løser dette problemet.
#
# ## Forutsetninger
# Vi bruker `pandas`, `polars` og `pyarrow` for å lese, skrive og analysere Parquet-dataene.

# %%
from decimal import ROUND_HALF_UP
from decimal import Decimal
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def show(df):
    """Viser en DataFrame tilpasset kjøremiljøet (display() i Jupyter, print() i skript)."""
    try:
        from IPython import get_ipython

        if get_ipython() is not None:
            from IPython.display import display

            display(df)
            return
    except (ImportError, NameError):
        pass
    print(df)


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
print(f"Python round(103.55, 1):                {round(float_val, 1)}")
print(
    f"Decimal ROUND_HALF_UP (avrunding):      {decimal_val.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)}"
)

# %% [markdown]
# ## 2. Store beløp og grensen for flyttalls-presisjon (2^53)
#
# En spesiell utfordring med flyttall oppstår når tallene blir svært store.
# Grensen for nøyaktig heltallsrepresentasjon i `float64` er nøyaktig $2^{53} = 9007199254740992$.
#
# Over denne grensen kan ikke flyttall representere partalls/oddetalls-forskjeller nøyaktig, og de mister helt evnen til å lagre desimaler (f.eks. øre).
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
# 2. **Kompakt Decimal-lagring** (`store_decimal_as_integer=True`), som bruker standard heltallstyper (`INT32` / `INT64`) for desimaler med presisjon < 18.

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

# Definer stier til testfiler (sjekker om vi kjører fra rotkatalogen eller fra src/decimal-mappen)
base_dir = Path("src/decimal") if Path("src/decimal").is_dir() else Path(".")
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
show(show_parquet_column_types(default_parquet))

# %%
print("=== Fysiske vs Logiske typer i decimal_as_int_example.parquet ===")
show(show_parquet_column_types(int_parquet))

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
show(df_read)

# %%
print("DataFrame dtypes:")
print(df_read.dtypes)

# %% [markdown]
# ## 6. Demonstrasjon med Polars
#
# Polars har førsteklasses støtte for desimaltall via `pl.Decimal`-datatypen, og kan lese og skrive de samme filene sømløst og interoperabelt med Pandas/PyArrow og R.
#
# ### 6.1 Lese Parquet-filer med Polars
#
# Vi kan lese de eksisterende Parquet-filene (opprettet av Pandas/PyArrow) direkte inn i Polars med `pl.read_parquet`.
# Polars oppdager automatisk desimal-kolonnene og leser dem som eksakte `Decimal`-typer med korrekt presisjon og skala.

# %%
import polars as pl

print("=== Lese standard desimalfil med Polars ===")
df_polars_read = pl.read_parquet(default_parquet)
show(df_polars_read)

# %%
print("Polars DataFrame-skjema (schema):")
for name, dtype in df_polars_read.schema.items():
    print(f"Col: {name:<20} Type: {dtype}")

# %% [markdown]
# ### 6.2 Verifisere de store beløpene i Polars
#
# Akkurat som med PyArrow og i R, kan Polars skille de to store beløpene over flyttallsgrensen ($2^{53}$) fordi de er lagret som eksakte desimaler, ikke flyttall.

# %%
belop_1 = df_polars_read["belop"][0]
belop_2 = df_polars_read["belop"][1]

print("=== Store verdier lest inn i Polars ===")
print(f"Verdi 1: {belop_1}")
print(f"Verdi 2: {belop_2}")
print(f"Er de to verdiene like i Polars? {belop_1 == belop_2}")

# %% [markdown]
# ### 6.3 Opprette en tilsvarende Polars DataFrame med desimaltyper
#
# Vi kan enkelt bygge en tilsvarende DataFrame i Polars og angi `pl.Decimal` med ønsket presisjon og skala i `schema`-parameteren.

# %%
df_polars_new = pl.DataFrame(
    {
        "item_id": [1, 2, 3, 4, 5],
        "amount_float64": [float(v) for v in raw_values],
        "amount_py_decimal": [Decimal(v) for v in raw_values],
        "amount_decimal_p8": [Decimal(v) for v in raw_values],
        "amount_decimal_p15": [Decimal(v) for v in raw_values],
        "amount_decimal_p25": [Decimal(v) for v in raw_values],
        "belop": [
            Decimal("9007199254740992.01"),
            Decimal("9007199254740992.02"),
            None,
            None,
            None,
        ],
    },
    schema={
        "item_id": pl.Int64,
        "amount_float64": pl.Float64,
        "amount_py_decimal": pl.Decimal(6, 2),
        "amount_decimal_p8": pl.Decimal(8, 2),
        "amount_decimal_p15": pl.Decimal(15, 2),
        "amount_decimal_p25": pl.Decimal(25, 2),
        "belop": pl.Decimal(18, 2),
    },
)

show(df_polars_new)

# %% [markdown]
# ### 6.4 Skrive og overskrive Parquet-filer med Polars
#
# Polars' innebygde Parquet-skriver (`write_parquet`) støtter desimaler direkte.
#
# **Viktig ytelsesdetalj:** Polars' native Parquet-skriver lagrer automatisk desimaler som kompakte heltall (`INT32` eller `INT64`) når presisjonen er 18 eller lavere (kompakt lagring). Dette skjer helt av seg selv.
#
# Hvis vi ønsker å tvinge standard `FIXED_LEN_BYTE_ARRAY`-lagring for lavere presisjoner (for å matche standardfilen nøyaktig), kan vi bruke PyArrow-motoren under panseret ved å sette `use_pyarrow=True` og sende med `pyarrow_options`.
#
# Vi demonstrerer begge deler ved å overskrive filene:

# %%
# 1. Skrive standard desimalfil (tvinge FIXED_LEN_BYTE_ARRAY med pyarrow)
df_polars_new.write_parquet(
    default_parquet,
    use_pyarrow=True,
    pyarrow_options={"store_decimal_as_integer": False},
)

# 2. Skrive kompakt desimalfil (Polars' native skriver gjør dette automatisk!)
df_polars_new.write_parquet(int_parquet)

print("Overskrevet de opprinnelige filene med Polars-generert Parquet!")

# %% [markdown]
# ### 6.5 Inspisere de Polars-genererte filene på disk
#
# Vi bruker den samme inspeksjons-funksjonen fra tidligere for å bekrefte at filene skrevet av Polars har nøyaktig de samme fysiske og logiske egenskapene!

# %%
print(
    "=== Fysiske vs Logiske typer i default_parquet skrevet med Polars (via PyArrow) ==="
)
show(show_parquet_column_types(default_parquet))

print("\n=== Fysiske vs Logiske typer i int_parquet skrevet natively med Polars ===")
show(show_parquet_column_types(int_parquet))

# %% [markdown]
# ### 6.6 Bekrefte full interoperabilitet med Pandas og R
#
# Siden Polars har skrevet standardiserte Parquet-filer, kan Pandas lese dem tilbake helt feilfritt med nøyaktig de samme datatypene og verdiene.
# For å teste med R kjører kommandoen: `Rscript src/decimal/verify_decimal_parquet.R`.

# %%
df_pandas_from_polars = pd.read_parquet(
    default_parquet, engine="pyarrow", dtype_backend="pyarrow"
)
print("Pandas leste fil skrevet av Polars:")
print(df_pandas_from_polars.dtypes)
show(df_pandas_from_polars)
