"""Testing Change Data Methods.
"""
from changelist_sort.change_data import ChangeData
from test.conftest import get_change_data


def test_get_sort_path_after_src_file_returns_after():
    expected = '/app/src/main/java/app/Main.java'
    test_data = ChangeData(
        after_dir=False,
        after_path=expected
    )
    assert expected == test_data._get_sort_path()


def test_get_sort_path_before_and_after_src_files_returns_after():
    expected = '/app/src/main/java/app/Main.java'
    test_data = ChangeData(
        before_dir=False,
        before_path='/app/src/main/java/app/File.java',
        after_dir=False,
        after_path=expected
    )
    assert expected == test_data._get_sort_path()


def test_get_sort_path_before_src_file_returns_before():
    expected = '/app/src/main/java/app/Main.java'
    test_data = ChangeData(
        before_dir=False,
        before_path=expected,
    )
    assert expected == test_data._get_sort_path()


def test_first_dir_root_gradle_returns_none(root_gradle_build_change_data):
    assert root_gradle_build_change_data.first_dir is None


def test_first_dir_app_gradle_returns_app(app_gradle_build_change_data):
    assert 'app' == app_gradle_build_change_data.first_dir


def test_first_dir_module_src_returns_module(module_src_change_data):
    assert 'module' == module_src_change_data.first_dir


def test_first_dir_module_test_returns_module(module_test_change_data):
    assert 'module' == module_test_change_data.first_dir


def test_first_dir_gradle_properties_returns_gradle(gradle_properties_change_data):
    assert 'gradle' == gradle_properties_change_data.first_dir


def test_first_dir_github_workflows_returns_github(github_workflows_change_data):
    assert '.github' == github_workflows_change_data.first_dir


def test_file_basename_module_src_file_returns_file(module_src_change_data):
    assert 'Main.java' == module_src_change_data.file_basename


def test_file_basename_gradle_properties_returns_file(gradle_properties_change_data):
    assert 'gradle-wrapper.properties' == gradle_properties_change_data.file_basename


def test_file_basename_root_gradle_build_returns_file(root_gradle_build_change_data):
    assert 'build.gradle' == root_gradle_build_change_data.file_basename


def test_file_ext_module_src_file_returns_ext(module_src_change_data):
    assert 'java' == module_src_change_data.file_ext


def test_file_ext_root_gradle_build_returns_ext(root_gradle_build_change_data):
    assert 'gradle' == root_gradle_build_change_data.file_ext


def test_file_ext_github_src_file_returns_ext(github_workflows_change_data):
    assert 'yml' == github_workflows_change_data.file_ext


def test_file_ext_hidden_file_with_ext_returns_ext():
    assert 'c' == get_change_data('/module/.hidden_file.c').file_ext


def test_file_ext_hidden_file_no_ext_returns_none():
    assert get_change_data('/module/.hidden_file').file_ext is None


def test_file_ext_gradle_kts_returns_ext():
    assert 'gradle.kts' == get_change_data('/module/build.gradle.kts').file_ext


def test_file_ext_gradlew_executable_returns_none():
    assert get_change_data('/gradlew').file_ext is None
