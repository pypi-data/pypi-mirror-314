""" Testing Developer File Pattern.
"""
from changelist_sort.sorting.sorting_file_pattern import SortingFilePattern

from test.conftest import get_change_data


def test_constructor_invalid_kwarg_raises_error():
    try:
        SortingFilePattern(invalid_kwarg='')
        raised_error = False
    except TypeError:
        raised_error = True
    assert raised_error


def test_constructor_empty_raises_exit():
    try:
        SortingFilePattern()
        raised_error = False
    except SystemExit:
        raised_error = True
    assert raised_error


def test_check_file_file_ext_returns_true(app_gradle_build_change_data):
    instance = SortingFilePattern(
        inverse=False,
        file_ext='gradle'
    )
    assert instance.check_file(
        app_gradle_build_change_data
    )


def test_check_file_file_ext_inverse_returns_false(app_gradle_build_change_data):
    instance = SortingFilePattern(
        inverse=True,
        file_ext='gradle'
    )
    assert not instance.check_file(
        app_gradle_build_change_data
    )


def test_check_file_first_dir_app_app_gradle_returns_true(app_gradle_build_change_data):
    instance = SortingFilePattern(
        inverse=False,
        first_dir='app'
    )
    assert instance.check_file(
        app_gradle_build_change_data
    )
    

def test_check_file_first_dir_gradle_app_gradle_returns_false(app_gradle_build_change_data):
    instance = SortingFilePattern(
        inverse=False,
        first_dir='gradle'
    )
    assert not instance.check_file(
        app_gradle_build_change_data
    )
    

def test_check_file_first_dir_app_inverse_app_gradle_returns_false(app_gradle_build_change_data):
    instance = SortingFilePattern(
        inverse=True,
        first_dir='app'
    )
    assert not instance.check_file(
        app_gradle_build_change_data
    )
    

def test_check_file_first_dir_gradle_inverse_app_gradle_returns_true(app_gradle_build_change_data):
    instance = SortingFilePattern(
        inverse=True,
        first_dir='gradle'
    )
    assert instance.check_file(
        app_gradle_build_change_data
    )
    

def test_check_file_filename_prefix_build_app_gradle_returns_true(app_gradle_build_change_data):
    instance = SortingFilePattern(
        inverse=False,
        filename_prefix='build'
    )
    assert instance.check_file(
        app_gradle_build_change_data
    )


def test_check_file_filename_prefix_build_inverse_app_gradle_returns_false(app_gradle_build_change_data):
    instance = SortingFilePattern(
        inverse=True,
        filename_prefix='build'
    )
    assert not instance.check_file(
        app_gradle_build_change_data
    )
    

def test_check_file_filename_suffix_build_app_gradle_returns_true(app_gradle_build_change_data):
    instance = SortingFilePattern(
        inverse=False,
        filename_suffix='build'
    )
    assert instance.check_file(
        app_gradle_build_change_data
    )


def test_check_file_filename_suffix_build_inverse_app_gradle_returns_false(app_gradle_build_change_data):
    instance = SortingFilePattern(
        inverse=True,
        filename_suffix='build'
    )
    assert not instance.check_file(
        app_gradle_build_change_data
    )


def test_check_file_filename_suffix_file_basename_is_none_returns_false():
    instance = SortingFilePattern(
        filename_suffix='build'
    )
    cd = get_change_data('/just/a/directory/')
    assert cd.file_basename == ''
    assert not instance.check_file(cd)


def test_check_file_path_start_github_github_workflows_returns_true(github_workflows_change_data):
    instance = SortingFilePattern(
        path_start='.github/'
    )
    assert instance.check_file(github_workflows_change_data)


def test_check_file_path_start_github_github_dependabot_returns_true(dependabot_change_data):
    instance = SortingFilePattern(
        path_start='.github/'
    )
    assert instance.check_file(dependabot_change_data)


def test_check_file_path_start_slash_char_github_github_dependabot_returns_true(dependabot_change_data):
    instance = SortingFilePattern(
        path_start='/.github/'
    )
    assert instance.check_file(dependabot_change_data)


def test_check_file_path_end_github_workflows_returns_true(github_workflows_change_data):
    instance = SortingFilePattern(
        path_end='workflows'
    )
    assert instance.check_file(github_workflows_change_data)


def test_check_file_path_end_workflows_github_workflows_returns_true(github_workflows_change_data):
    instance = SortingFilePattern(
        path_end='/workflows'
    )
    assert instance.check_file(github_workflows_change_data)


def test_check_file_path_end_workflows_github_dependabot_returns_false(dependabot_change_data):
    instance = SortingFilePattern(
        path_end='/workflows'
    )
    assert not instance.check_file(dependabot_change_data)
