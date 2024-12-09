""" Testing String Validation Methods
"""

from changelist_sort.input.string_validation import validate_name


def test_validate_name_empty_returns_false():
    assert not validate_name('')


def test_validate_name_space_returns_false():
    assert not validate_name(' ')


def test_validate_name_simple_returns_true():
    assert validate_name('a')


def test_validate_name_non_string_returns_false():
    assert not validate_name(2)
