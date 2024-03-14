import pytest

from pytest_examples.functions import is_prime


def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(4) is False
    assert is_prime(0) is False
    assert is_prime(-5) is False

    with pytest.raises(TypeError) as excinfo:
        is_prime(3.5)
    assert str(excinfo.value) == "Number must be an integer."
