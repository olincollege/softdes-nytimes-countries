"""
This module deals with testing some of the functions in the processing module.
"""
import pytest
from processing import headline_list_to_string, all_headlines_in_string

HEADLINE_LIST_TO_STRING_CASES = [
    ("201801", "Test Headline Test headline 2"), #Tests that comma/list element
                                                 #is removed
    ("201802", "Here 'a' headline"), #Tests that apostrophe removed, not quote
]
@pytest.mark.parametrize("test_input,expected", HEADLINE_LIST_TO_STRING_CASES)
def test_days_of_month(test_input, expected):
    """
    Test that the function headline_list_to_string returns the expected string
    with appropriate processing of commas and quotation marks.

    The specific test cases are commented above next to the variable
    HEADLINE_LIST_TO_STRING_CASES.
    """
    assert headline_list_to_string("test", test_input) == expected

ALL_HEADLINES_TO_STRING_CASES = [
    ("test", "Test Headline Test headline 2 Here 'a' headline More testing"),
                                    #Tests that all three months are combined
]
@pytest.mark.parametrize("test_input,expected", ALL_HEADLINES_TO_STRING_CASES)
def test_all_headlines_in_string(test_input, expected):
    """
    Test that the function all_headlines_in_string returns the expected string
    containing all of the headlines combined.

    The specific test cases are commented above next to the variable
    ALL_HEADLINES_TO_STRING_CASES.
    """
    assert all_headlines_in_string(test_input) == expected
