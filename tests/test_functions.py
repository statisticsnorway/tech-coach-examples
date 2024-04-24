from pathlib import Path

import pandas as pd
import pytest
from pandas import testing as tm

from pytest_examples.functions import is_prime, valuta_omv


def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(4) is False
    assert is_prime(0) is False
    assert is_prime(-5) is False

    with pytest.raises(TypeError) as excinfo:
        is_prime(3.5)
    assert str(excinfo.value) == "Number must be an integer."


def test_valuta_omv(inndata, val_data):
    result_df = valuta_omv(inndata, val_data)

    facit_file = Path(__file__).parent / "testdata" / "valuta_omv_facit.parquet"
    facit_df = pd.read_parquet(facit_file)
    tm.assert_frame_equal(result_df, facit_df)
