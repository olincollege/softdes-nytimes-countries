import pytest
from processing import headline_list_to_string, all_headlines_in_string

HEADLINE_LIST_TO_STRING_CASES = [
    ("201801", "Test Headline Test headline 2"),
]
@pytest.mark.parametrize("test_input,expected", HEADLINE_LIST_TO_STRING_CASES)
def test_days_of_month(test_input, expected):
    print(test_input[0])
    assert headline_list_to_string("test", test_input) == expected

