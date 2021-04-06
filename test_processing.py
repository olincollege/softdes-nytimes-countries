import pytest
from processing import headline_list_to_string, all_headlines_in_string

HEADLINE_LIST_TO_STRING_CASES = [
    ("201801", "Test Headline Test headline 2"), #Tests that comma/list element
                                                 #is removed
    ("201802", "Here 'a' headline"), #Tests that apostrophe removed, not quote
]
@pytest.mark.parametrize("test_input,expected", HEADLINE_LIST_TO_STRING_CASES)
def test_days_of_month(test_input, expected):
    assert headline_list_to_string("test", test_input) == expected

ALL_HEADLINES_TO_STRING_CASES = [
    ("test", "Test Headline Test headline 2 Here 'a' headline More testing"), 
                                    #Tests that all three months are combined
]
@pytest.mark.parametrize("test_input,expected", ALL_HEADLINES_TO_STRING_CASES)
def test_all_headlines_in_string(test_input, expected):
    assert all_headlines_in_string(test_input) == expected


