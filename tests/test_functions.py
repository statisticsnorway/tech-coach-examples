import pandas as pd
from pandas import testing as tm

from pytest_examples.functions import flatten_col_multiindex, is_prime


def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(4) is False
    assert is_prime(0) is False
    assert is_prime(-5) is False


#    with pytest.raises(TypeError) as excinfo:
#        is_prime(3.5)
#    assert str(excinfo.value) == "Number must be an integer."


def test_flatten_col_multiindex(multiindex: pd.DataFrame) -> None:
    multiindex.to_csv("multiindex.csv")
    result = flatten_col_multiindex(multiindex)
    result.to_csv("result.csv")
    assert tm.assert_frame_equal(result, multiindex)
