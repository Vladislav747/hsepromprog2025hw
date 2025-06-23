import pytest
from src.simple_library_01.functions import get_month_days


def test_get_month_days():
    assert get_month_days(1930, 1) == 30
    assert get_month_days(1930, 2) == 30
    assert get_month_days(1931, 2) == 28
    assert get_month_days(2000, 2) == 29


@pytest.mark.parametrize("year, month, expected", [
    (2020, 2, 29),   # високосный февраль
    (2021, 2, 28),    # невисокосный февраль
    (2023, 1, 31),    # январь
    (2023, 4, 30),    # апрель
    (1930, 5, 30),    # особый 1930 год
    (2000, 2, 29),    # вековой високосный
    (1900, 2, 28),    # вековой невисокосный
])
def test_month_days_with_parameters(year, month, expected):
    assert get_month_days(year, month) == expected

def test_invalid_months():
    with pytest.raises(AttributeError):
        get_month_days(2023, 0)
    with pytest.raises(AttributeError):
        get_month_days(2023, 13)
    with pytest.raises(AttributeError):
        get_month_days(2023, -5)