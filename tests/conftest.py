from pathlib import Path

# Store testdata for the valuta_omv function
import pandas as pd
import pytest


@pytest.fixture
def inndata() -> pd.DataFrame:
    inndata_file = Path(__file__).parent / "testdata" / "valuta_omv_inndata.parquet"
    inndata_df = pd.read_parquet(inndata_file)

    return inndata_df


@pytest.fixture
def val_data() -> pd.DataFrame:
    exchange_rates_file = (
        Path(__file__).parent / "testdata" / "valuta_omv_exchange_rates.parquet"
    )
    exchange_df = pd.read_parquet(exchange_rates_file)
    return exchange_df
