""" Testing List Sort Methods.
    The method split_changelist requires a callable arg, which applies the module sort for now.
"""
from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_data import ChangelistData
from changelist_sort.sorting import module_sort
from changelist_sort.sorting.list_sort import split_changelist


def test_split_changelist_empty_returns_empty():
    test_input = ChangelistData(
        id='1234',
        name='Empty',
    )
    result_list = split_changelist(test_input, module_sort.is_sorted_by_module)
    assert len(test_input.changes) == 0
    assert len(result_list) == 0


def test_split_changelist_module_sorted_returns_sorted(module_src_change_data, module_test_change_data):
    test_input = ChangelistData(
        id='1234',
        name='Module',
        changes=[
            module_src_change_data,
            module_test_change_data,
        ],
    )
    result_list = split_changelist(test_input, module_sort.is_sorted_by_module)
    assert len(test_input.changes) == 2
    assert len(result_list) == 0


def test_split_changelist_build_updates_sorted_returns_sorted():
    test_input = ChangelistData(
        id='1234',
        name='Build Updates',
        changes=[
            ChangeData(
                after_dir=False,
                after_path='/app/build.gradle',
            ),
        ],
    )
    result_list = split_changelist(test_input, module_sort.is_sorted_by_module)
    assert len(test_input.changes) == 1
    assert len(result_list) == 0


def test_split_changelist_unsorted_returns_split():
    test_input = ChangelistData(
        id='1234',
        name='App',
        changes=[
            ChangeData(
                after_dir=False,
                after_path='/module/src/main/java/module/Main.java',
            ),
        ],
    )
    result_list = split_changelist(test_input, module_sort.is_sorted_by_module)
    assert len(test_input.changes) == 0
    assert len(result_list) == 1


def test_split_changelist_half_sorted_returns_split():
    test_cd0 = ChangeData(
        after_dir=False,
        after_path='/module/src/main/java/module/Main.java',
    )
    test_cd1 = ChangeData(
        after_dir=False,
        after_path='/app/src/main/java/app/Main.java',
    )
    test_input = ChangelistData(
        id='1234',
        name='App',
        changes=[test_cd0, test_cd1],
    )
    result_list = split_changelist(test_input, module_sort.is_sorted_by_module)
    assert len(test_input.changes) == 1
    assert test_input.changes[0] == test_cd1
    assert len(result_list) == 1
    assert result_list[0] == test_cd0


def test_split_changelist_root_unsorted_returns_unsorted():
    test_cd0 = ChangeData(
        after_dir=False,
        after_path='/app/Main.java',
    )
    test_input = ChangelistData(
        id='1234',
        name='Root',
        changes=[test_cd0],
    )
    result_list = split_changelist(test_input, module_sort.is_sorted_by_module)
    assert len(test_input.changes) == 0
    assert len(result_list) == 1
    assert test_cd0 == result_list[0]


def test_split_changelist_project_root_sorted_returns_sorted():
    test_cd0 = ChangeData(
        after_dir=False,
        after_path='/Main.java',
    )
    test_input = ChangelistData(
        id='1234',
        name='Project Root',
        changes=[test_cd0],
    )
    result_list = split_changelist(test_input, module_sort.is_sorted_by_module)
    assert len(test_input.changes) == 1
    assert test_input.changes[0] == test_cd0
    assert len(result_list) == 0


def test_split_changelist_root_sorted_returns_sorted():
    test_cd0 = ChangeData(
        after_dir=False,
        after_path='/Main.java',
    )
    test_input = ChangelistData(
        id='1234',
        name='Root',
        changes=[test_cd0],
    )
    result_list = split_changelist(test_input, module_sort.is_sorted_by_module)
    assert len(test_input.changes) == 1
    assert test_input.changes[0] == test_cd0
    assert len(result_list) == 0


def test_split_changelist_build_updates_unsorted_returns_sorted(
    module_src_change_data,
    module_test_change_data,
    github_workflows_change_data,
    dependabot_change_data
):
    test_input = ChangelistData(
        id='1234',
        name='Build Updates',
        changes=[
            module_src_change_data,
            module_test_change_data,
            github_workflows_change_data,
            dependabot_change_data,
        ],
    )
    result_list = split_changelist(test_input, module_sort.is_sorted_by_module)
    assert len(test_input.changes) == 0
    assert len(result_list) == 4
