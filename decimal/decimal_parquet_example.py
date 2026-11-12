"""Example showing the Decimal type stored in Parquet files vs float.

Demonstrates why Decimal is preferable to float (IEEE 754 binary64) when exact
representation and deterministic rounding are important (e.g., 103.55), how to
store and read Decimal columns using pandas and PyArrow, and how to inspect the
logical and physical types of columns in a Parquet file.
"""

from decimal import ROUND_HALF_UP
from decimal import Decimal
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def demonstrate_float_vs_decimal() -> None:
    """Show why float fails on exact representation and rounding for numbers like 103.55."""
    float_val = 103.55
    decimal_val = Decimal("103.55")

    print("=== 1. Exact Representation: float vs Decimal ===")
    print(f"Float 103.55 formatted to 50 decimals:   {float_val:.50f}")
    print(f"Decimal('103.55') exact value:           {decimal_val}")
    print()

    print("=== 1.5. Large Values and float64 Precision Limits ===")
    # 9007199254740992 is 2^53, the limit of exact representation for float64.
    # Beyond this, floats cannot represent small fractional differences like 0.01 or 0.02.
    float_large_1 = float("9007199254740992.01")
    float_large_2 = float("9007199254740992.02")
    decimal_large_1 = Decimal("9007199254740992.01")
    decimal_large_2 = Decimal("9007199254740992.02")
    print(f"Float 9007199254740992.01:               {float_large_1}")
    print(f"Float 9007199254740992.02:               {float_large_2}")
    print(f"Are the two floats equal?                {float_large_1 == float_large_2}")
    print(f"Decimal 9007199254740992.01:             {decimal_large_1}")
    print(f"Decimal 9007199254740992.02:             {decimal_large_2}")
    print(f"Are the two Decimals equal?              {decimal_large_1 == decimal_large_2}")
    print()

    print("=== 2. Rounding to 1 decimal place ===")
    # In binary floating-point, 103.55 is stored as ~103.549999999999997158...
    # Because it is slightly less than halfway (103.55), round(103.55, 1) rounds DOWN to 103.5
    # even though conceptually we want it to round to 103.6.
    print(f"Python round(float(103.55), 1):          {round(float_val, 1)}")
    print(
        f"Decimal('103.55') ROUND_HALF_UP (0.1):   {decimal_val.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)}"
    )
    print()

    print("=== 3. Arithmetic accumulation errors ===")
    print(
        f"Float:   103.55 + 0.1 = {103.55 + 0.1!r} (== 103.65: {103.55 + 0.1 == 103.65})"
    )
    print(
        f"Decimal: 103.55 + 0.1 = {Decimal('103.55') + Decimal('0.1')} "
        f"(== 103.65: {Decimal('103.55') + Decimal('0.1') == Decimal('103.65')})"
    )
    print(f"Float:   103.55 * 3   = {103.55 * 3!r} (== 310.65: {103.55 * 3 == 310.65})")
    print(
        f"Decimal: 103.55 * 3   = {Decimal('103.55') * 3} "
        f"(== 310.65: {Decimal('103.55') * 3 == Decimal('310.65')})"
    )
    print()


def create_decimal_parquet(
    parquet_path: Path, store_decimal_as_integer: bool = False
) -> pd.DataFrame:
    """Create a DataFrame with float and Decimal columns and save it to a Parquet file.

    Args:
        parquet_path: Destination path for the Parquet file.
        store_decimal_as_integer: If True, Parquet stores decimals with precision <= 18
            as physical INT32/INT64 instead of FIXED_LEN_BYTE_ARRAY.

    Returns:
        The created pandas DataFrame.
    """
    raw_values = ["103.55", "10.05", "1.15", "2.55", "1999.95"]

    df = pd.DataFrame(
        {
            "item_id": pd.Series([1, 2, 3, 4, 5], dtype="int64[pyarrow]"),
            "amount_float64": pd.Series(
                [float(v) for v in raw_values], dtype="float64"
            ),
            # Python Decimal objects in a column (automatically inferred by PyArrow as decimal128)
            "amount_py_decimal": [Decimal(v) for v in raw_values],
            # Explicit PyArrow decimal128 with precision=8, scale=2
            "amount_decimal_p8": pd.Series(
                [Decimal(v) for v in raw_values],
                dtype=pd.ArrowDtype(pa.decimal128(8, 2)),
            ),
            # Explicit PyArrow decimal128 with precision=15, scale=2
            "amount_decimal_p15": pd.Series(
                [Decimal(v) for v in raw_values],
                dtype=pd.ArrowDtype(pa.decimal128(15, 2)),
            ),
            # Explicit PyArrow decimal128 with precision=25, scale=2
            "amount_decimal_p25": pd.Series(
                [Decimal(v) for v in raw_values],
                dtype=pd.ArrowDtype(pa.decimal128(25, 2)),
            ),
            # Explicit PyArrow decimal128 with precision=18, scale=2 (showing precision beyond float64)
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

    df.to_parquet(
        parquet_path,
        engine="pyarrow",
        index=False,
        store_decimal_as_integer=store_decimal_as_integer,
    )
    return df


def show_parquet_column_types(parquet_path: str | Path) -> pd.DataFrame:
    """Show the logical and physical types of all columns stored in a Parquet file.

    Args:
        parquet_path: Path to the Parquet file.

    Returns:
        A pandas DataFrame summarizing column names, physical types, logical types,
        Arrow types, precision, scale, and byte length.
    """
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
                "converted_type": col_schema.converted_type,
                "arrow_type": str(arrow_field.type),
                "precision": col_schema.precision,
                "scale": col_schema.scale,
                "type_length": col_schema.length,
            }
        )

    summary_df = pd.DataFrame(rows)
    print(f"=== Parquet Column Types for '{Path(parquet_path).name}' ===")
    print(summary_df.to_string(index=False))
    print()
    return summary_df


def compare_rounding_from_parquet(parquet_path: str | Path) -> None:
    """Read back the Parquet file and compare rounding on float vs Decimal columns."""
    # Read with dtype_backend="pyarrow" so Decimal columns remain Arrow decimal128
    df = pd.read_parquet(parquet_path, engine="pyarrow", dtype_backend="pyarrow")

    print("=== 4. Data Read Back from Parquet ===")
    print(df)
    print("\nDataFrame dtypes:")
    print(df.dtypes)
    print()

    # Compare rounding to 1 decimal place
    df_comparison = pd.DataFrame(
        {
            "original_exact": df["amount_decimal_p15"],
            "float_binary_exact": [
                f"{float(val):.20f}" for val in df["amount_float64"]
            ],
            "python_float_round": [
                round(float(val), 1) for val in df["amount_float64"]
            ],
            "decimal_round_half_up": [
                Decimal(str(val)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
                for val in df["amount_decimal_p15"]
            ],
        }
    )

    print("=== 5. Rounding Comparison (1 decimal place) ===")
    print(df_comparison.to_string(index=False))
    print()


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    default_parquet = base_dir / "decimal_example.parquet"
    int_parquet = base_dir / "decimal_as_int_example.parquet"

    demonstrate_float_vs_decimal()

    # 1. Default Parquet Decimal storage (FIXED_LEN_BYTE_ARRAY)
    create_decimal_parquet(default_parquet, store_decimal_as_integer=False)
    show_parquet_column_types(default_parquet)

    # 2. Parquet Decimal storage with store_decimal_as_integer=True (INT32 / INT64 for p <= 18)
    create_decimal_parquet(int_parquet, store_decimal_as_integer=True)
    show_parquet_column_types(int_parquet)

    compare_rounding_from_parquet(default_parquet)
