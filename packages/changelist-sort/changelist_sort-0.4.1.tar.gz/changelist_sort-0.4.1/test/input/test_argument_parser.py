"""Testing Argument Parser Methods.
"""
from changelist_sort.input.argument_parser import parse_arguments


def test_parse_arguments_empty_list_returns_none():
    result = parse_arguments()
    assert result.workspace_path is None


def test_parse_arguments_empty_str_returns_none():
    result = parse_arguments('')
    assert result.workspace_path is None


def test_parse_arguments_change_list_main_empty_changelist_arg():
    try:
        parse_arguments(['--changelist', ''])
        assert False
    except SystemExit:
        assert True


def test_parse_arguments_change_list_main_empty_workspace_arg():
    try:
        parse_arguments(['--workspace', ''])
        assert False
    except SystemExit:
        assert True


def test_parse_arguments_changelists_cl():
    result = parse_arguments(['--changelists', 'data.xml'])
    assert result.changelists_path == 'data.xml'
    assert result.workspace_path is None


def test_parse_arguments_workspace_cl():
    result = parse_arguments(['--workspace', 'workspace.xml'])
    assert result.changelists_path is None
    assert result.workspace_path == 'workspace.xml'


def test_parse_arguments_sourceset_short_flag():
    result = parse_arguments(['-s'])
    assert result.workspace_path is None
    assert result.sourceset_sort


def test_parse_arguments_sourceset_long():
    result = parse_arguments(['--sourceset-sort'])
    assert result.workspace_path is None
    assert result.sourceset_sort


def test_parse_arguments_sourceset_long2():
    result = parse_arguments(['--sourceset_sort'])
    assert result.workspace_path is None
    assert result.sourceset_sort


def test_parse_arguments_remove_empty_short_flag():
    result = parse_arguments(['-r'])
    assert result.workspace_path is None
    assert not result.sourceset_sort
    assert result.remove_empty


def test_parse_arguments_remove_empty_long():
    result = parse_arguments(['--remove-empty'])
    assert result.workspace_path is None
    assert not result.sourceset_sort
    assert result.remove_empty


def test_parse_arguments_remove_empty_long2():
    result = parse_arguments(['--remove_empty'])
    assert result.workspace_path is None
    assert not result.sourceset_sort
    assert result.remove_empty
