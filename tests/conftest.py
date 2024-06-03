from pathlib import Path

# Store testdata for the valuta_omv function
import pandas as pd
import pytest


@pytest.fixture
def inndata() -> pd.DataFrame:
    inndata_file = Path(__file__).parent / "testdata" / "valuta_omv_inndata.parquet"
    return pd.read_parquet(inndata_file)


@pytest.fixture
def val_data() -> pd.DataFrame:
    exchange_rates_file = (
        Path(__file__).parent / "testdata" / "valuta_omv_exchange_rates.parquet"
    )
    return pd.read_parquet(exchange_rates_file)
