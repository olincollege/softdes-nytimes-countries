import pytest
from data_processing_helpers import days_in_month, next_month

DAYS_IN_MONTH_CASES = [
    ("200002", "29"), #Tests that leap years have 29 days in February
]

@pytest.mark.parametrize("test_input,expected", DAYS_IN_MONTH_CASES)
def test_days_of_month(test_input, expected):
    assert days_in_month(test_input) == expected