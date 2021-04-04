import pytest
from data_processing_helpers import days_in_month, next_month, headline_list_to_string, all_headlines_in_string

DAYS_IN_MONTH_CASES = [
    ("200002", "29"), #Tests that leap years have 29 days in February
    ("200102", "28"), #Tests that non-leap years have 28 in February
    ("200001", "31"), #Tests that leap years do not have other months affected
    ("200101", "31"), #Tests that non-leap years have correct number of days
]

@pytest.mark.parametrize("test_input,expected", DAYS_IN_MONTH_CASES)
def test_days_of_month(test_input, expected):
    assert days_in_month(test_input) == expected

NEXT_MONTH_CASES = [
    ("199912", "200001"), #Tests that years go from 1999 to 2000 in December
    ("200012", "200101"), #Tests that year will increase for December input
    ("200001", "200002"), #Tests that month increases by 1
    ("200009", "200010"), #Tests that month can increase from one to two digits
]

@pytest.mark.parametrize("test_input,expected", NEXT_MONTH_CASES)
def test_next_month(test_input, expected):
    assert next_month(test_input) == expected

#HEADLINE_LIST_TO_STRING_CASES = [
#    ([])
#]
