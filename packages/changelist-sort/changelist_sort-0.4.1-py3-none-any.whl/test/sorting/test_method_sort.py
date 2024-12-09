""" Testing Sorting Package Init Methods.
"""
from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_data import ChangelistData
from changelist_sort.sorting import sort
from changelist_sort.sorting.sort_mode import SortMode

from test.conftest import APP_GRADLE_PATH, GRADLE_PROPERTIES_PATH, ROOT_GRADLE_PATH


def test_sort_empty_returns_empty():
    test_input = []
    result = sort(test_input, SortMode.MODULE)
    assert result == test_input


def test_sort_empty_invalid_sort_mode_raises_exit():
    try:
        sort([], 'sort_mode.invalid')
        raised_exit = False
    except SystemExit:
        raised_exit = True
    assert raised_exit


def test_sort_invalid_sort_mode_raises_exit(app_changelist):
    test_input = [app_changelist]
    try:
        sort(test_input, 'sort_mode.invalid')
        raised_exit = False
    except SystemExit:
        raised_exit = True
    assert raised_exit


def test_sort_no_changes_returns_same():
    test_input = [
        ChangelistData(
            id='1234',
            name='Gradle',
            changes=[],
        )
    ]
    assert test_input == sort(test_input, SortMode.MODULE)


def test_sort_gradle_cl_gradle_file_returns_unchanged():
    test_input = [
        ChangelistData(
            id='1234',
            name='Gradle',
            changes=[
                ChangeData(
                    after_path=APP_GRADLE_PATH,
                    after_dir=False,
                ),
            ],
        )
    ]
    assert test_input == sort(test_input, SortMode.MODULE)


def test_sort_gradle_cl_gradle_files_returns_unchanged():
    test_input = [
        ChangelistData(
            id='1234',
            name='Build Updates',
            changes=[
                ChangeData(
                    after_path=APP_GRADLE_PATH,
                    after_dir=False,
                ),
                ChangeData(
                    after_path=ROOT_GRADLE_PATH,
                    after_dir=False,
                ),
                ChangeData(
                    after_path=GRADLE_PROPERTIES_PATH,
                    after_dir=False,
                ),
            ],
        )
    ]
    assert test_input == sort(test_input, SortMode.MODULE)


def test_sort_app_cl_gradle_file_returns_new_gradle_cl(app_gradle_build_change_data):
    test_input = [
        ChangelistData(
            id='1234',
            name='App',
            changes=[app_gradle_build_change_data],
        )
    ]
    result = sort(test_input, SortMode.MODULE)
    assert result != test_input
    assert len(result) == 2
    assert result[0].name == 'App'
    assert result[1].name == 'Build Updates'
    # Check Contents of Changes List
    assert len(result[0].changes) == 0
    assert len(result[1].changes) == 1
    assert result[1].changes[0].after_path == APP_GRADLE_PATH


def test_sort_app_cl_gradle_file_sourceset_mode_returns_new_gradle_cl(app_gradle_build_change_data):
    test_input = [
        ChangelistData(
            id='1234',
            name='App',
            changes=[app_gradle_build_change_data],
        )
    ]
    result = sort(test_input, SortMode.SOURCESET)
    assert result != test_input
    assert len(result) == 2
    assert result[0].name == 'App'
    assert result[1].name == 'Build Updates'
    # Check Contents of Changes List
    assert len(result[0].changes) == 0
    assert len(result[1].changes) == 1
    assert result[1].changes[0].after_path == APP_GRADLE_PATH


def test_sort_module_cl_sourceset_mode_returns_new_sourceset_cl(
    module_changelist,
    module_src_change_data,
    module_test_change_data
):
    module_changelist.changes.append(module_src_change_data)
    module_changelist.changes.append(module_test_change_data)
    test_input = [module_changelist]
    result = sort(test_input, SortMode.SOURCESET)
    #
    assert result != test_input
    assert len(result) == 3
    assert result[0].name == 'Module'
    assert result[1].name == 'Module Test'
    assert result[2].name == 'Module Main'
    # Check Files
    assert len(result[0].changes) == 0
    assert len(result[1].changes) == 1
    assert len(result[2].changes) == 1


def test_sort_dev_empty_returns_empty(
    sort_config_developer_cl_0
):
    test_input = []
    result = sort(test_input, SortMode.MODULE, sort_config_developer_cl_0)
    assert len(result) == 0


def test_sort_dev_build_updates_cl_module_mode_returns_sorted(
    build_updates_changelist,
    sort_config_developer_cl_0
):
    test_input = [build_updates_changelist]
    result = sort(test_input, SortMode.MODULE, sort_config_developer_cl_0)
    assert len(result) == 1
    assert len(result[0].changes) == 1


def test_sort_dev_build_updates_cl_sorted_returns_sorted(
    build_updates_changelist,
    sort_config_developer_cl_0,
):
    test_input = [build_updates_changelist]
    result = sort(test_input, SortMode.MODULE, sort_config_developer_cl_0)
    assert len(result) == 1
    assert len(result[0].changes) == 1
