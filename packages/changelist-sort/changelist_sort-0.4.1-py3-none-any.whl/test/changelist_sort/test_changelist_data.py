""" Testing Changelist Data Methods
"""
from changelist_sort.changelist_data import ChangelistData


def test_list_key_empty_returns_empty():
    instance = ChangelistData(
        id='1234',
        name='',
        changes=[],
    )
    assert '' == instance.list_key.key


def test_list_key_space_returns_empty():
    instance = ChangelistData(
        id='1234',
        name=' ',
        changes=[],
    )
    assert '' == instance.list_key.key


def test_list_key_allcaps_returns_lower():
    instance = ChangelistData(
        id='1234',
        name='ALLCAPS',
        changes=[],
    )
    assert 'allcaps' == instance.list_key.key


def test_list_key_trailspace_returns_word():
    instance = ChangelistData(
        id='1234',
        name='Trailspace ',
        changes=[],
    )
    assert 'trailspace' == instance.list_key.key
