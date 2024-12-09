""" Testing Input Package Init Module Methods.
"""
from pathlib import Path
from unittest.mock import Mock

import pytest

from changelist_data.storage import StorageType, storage_type

from changelist_sort.input import validate_input
from changelist_sort.sorting.sort_mode import SortMode


def test_validate_input_no_args_ws_file_does_not_exist_raises_exit(monkeypatch):
    test_input = []
    monkeypatch.setattr(Path, 'exists', lambda _: False)
    #
    result = validate_input(test_input)
    #
    assert len(result.storage.get_changelists()) == 0
    assert result.storage.storage_type == StorageType.CHANGELISTS
    assert result.storage.update_path == storage_type.get_default_path(StorageType.CHANGELISTS)
    #
    assert result.sort_mode == SortMode.MODULE
    assert not result.remove_empty


def test_validate_input_no_args_ws_file_is_empty_raises_exit(monkeypatch):
    test_input = []
    monkeypatch.setattr(Path, 'exists', lambda _: True)
    monkeypatch.setattr(Path, 'read_text', lambda _: '')
    result = validate_input(test_input)
    assert len(result.storage.get_changelists()) == 0


def test_validate_input_no_args_ws_file_has_no_cl_(no_changelist_xml):
    test_input = []
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda p: p.name == '.idea/workspace.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: no_changelist_xml)
        result = validate_input(test_input)
    assert len(result.storage.get_changelists()) == 0


def test_validate_input_no_args_ws_file_simple_cl_(get_cl_simple_xml):
    test_input = []
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda p: True)
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: get_cl_simple_xml)
        result = validate_input(test_input)
    assert len(result.storage.get_changelists()) == 1


def test_validate_input_no_args_ws_file_multi_cl_(multi_storage, get_cl_multi_xml):
    test_input = []
    def storage_expects(storage_type, path):
        if storage_type is not None:
            exit("Provided Storage Type was None")
        if path is not None:
            exit("Provided Path was None")
        return multi_storage
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda p: True)
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: get_cl_multi_xml)
        result = validate_input(test_input)
        assert len(result.storage.get_changelists()) == 2



def test_validate_input_ws_path_arg_is_empty_raises_exit(no_changelist_xml):
    test_input = ['--workspace', '']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: no_changelist_xml)
        try:
            validate_input(test_input)
            assert False
        except SystemExit:
            assert True


def test_validate_input_ws_path_arg_is_missing_raises_exit(no_changelist_xml):
    test_input = ['--workspace']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: no_changelist_xml)
        try:
            validate_input(test_input)
            assert False
        except SystemExit:
            assert True


def test_validate_input_ws_path_arg_does_not_exist_raises_exit():
    test_input = ['--workspace', '/file.xml']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: False)
        try:
            validate_input(test_input)
            assert False
        except SystemExit:
            assert True


def test_validate_input_sourceset_sort(no_changelist_xml):
    test_input = ['-s']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda p: p.name == '.idea/workspace.xml')
        c.setattr(Path, 'read_text', lambda _: no_changelist_xml)
        result = validate_input(test_input)
        #
        assert result.sort_mode == SortMode.SOURCESET
        #
        assert len(result.storage.get_changelists()) == 0


def test_validate_input_remove_empty(no_changelist_xml):
    test_input = ['-r']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda p: p.name == '.idea/workspace.xml')
        c.setattr(Path, 'read_text', lambda _: no_changelist_xml)
        result = validate_input(test_input)
        #
        assert result.sort_mode == SortMode.MODULE
        assert result.remove_empty
        assert len(result.storage.get_changelists()) == 0
