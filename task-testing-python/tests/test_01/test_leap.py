import pytest
from src.simple_library_01.functions import is_leap

def test_non_leap_year():
    assert is_leap(2021) == False
    assert is_leap(2019) == False
    assert is_leap(1900) == False


def test_invalid_years():
    with pytest.raises(AttributeError):
        is_leap(0)
    with pytest.raises(AttributeError):
        is_leap(-100)
    with pytest.raises(AttributeError):
        is_leap(-1)


@pytest.mark.parametrize("year, expected", [
    (2000, True),
    (2004, True),
    (2020, True),
    (1900, False),
    (2021, False),
    (2100, False),
])
def test_leap_years_with_parameters(year, expected):
    assert is_leap(year) == expected