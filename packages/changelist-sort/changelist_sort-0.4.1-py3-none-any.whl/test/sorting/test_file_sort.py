""" Testing Change Sort Module Methods
"""
from changelist_sort.change_data import ChangeData
from changelist_sort.sorting.file_sort import get_module_name, get_module_type
from changelist_sort.sorting.module_type import ModuleType

from test.conftest import get_change_data, GRADLE_PROPERTIES_PATH, GITHUB_WORKFLOW_PATH


def test_get_module_name_empty_returns_none():
    assert get_module_name(ChangeData()) is None


def test_get_module_name_requirements_file_returns_module():
    assert 'root' == get_module_name(
        get_change_data('requirements.txt')
    )


def test_get_module_name_setup_file_returns_module():
    assert 'root' == get_module_name(
        get_change_data('setup.py')
    )


def test_get_module_name_src_file_returns_module(module_src_change_data):
    assert 'module' == get_module_name(module_src_change_data)
    

def test_get_module_name_test_file_returns_module(module_test_change_data):
    assert 'module' == get_module_name(module_test_change_data)


def test_get_module_name_app_build_file_returns_app(app_gradle_build_change_data):
    assert 'gradle' == get_module_name(app_gradle_build_change_data)


def test_get_module_name_root_build_file_returns_root(root_gradle_build_change_data):
    assert 'gradle' == get_module_name(root_gradle_build_change_data)


def test_get_module_name_github_workflows_returns_github(github_workflows_change_data):
    assert 'github' == get_module_name(github_workflows_change_data)


def test_get_module_name_github_dependabot_returns_github(dependabot_change_data):
    assert 'github' == get_module_name(dependabot_change_data)


def test_get_module_type_root_gradle_returns_gradle(root_gradle_build_change_data):
    assert ModuleType.GRADLE == get_module_type(root_gradle_build_change_data)


def test_get_module_type_root_gradle_kts_returns_gradle():
    assert ModuleType.GRADLE == get_module_type(get_change_data('/build.gradle.kts'))


def test_get_module_type_gradle_properties_returns_gradle():
    assert ModuleType.GRADLE == get_module_type(get_change_data(GRADLE_PROPERTIES_PATH))


def test_get_module_type_app_build_file_returns_module(app_gradle_build_change_data):
    assert ModuleType.GRADLE == get_module_type(app_gradle_build_change_data)


def test_get_module_type_module_src_cd_returns_module(module_src_change_data):
    assert ModuleType.MODULE == get_module_type(module_src_change_data)


def test_get_module_type_module_test_cd_returns_module(module_test_change_data):
    assert ModuleType.MODULE == get_module_type(module_test_change_data)


def test_get_module_type_module_debug_cd_returns_module(module_debug_change_data):
    assert ModuleType.MODULE == get_module_type(module_debug_change_data)


def test_get_module_type_app_src_file_returns_module():
    assert ModuleType.MODULE == get_module_type(
        get_change_data('/app/src/main/java/com/example/app/Main.java')
    )


def test_get_module_type_app_test_file_returns_module():
    assert ModuleType.MODULE == get_module_type(
        get_change_data('/app/src/test/java/com/example/app/Main.java')
    )


def test_get_module_type_app_res_file_returns_module():
    assert ModuleType.MODULE == get_module_type(
        get_change_data('/app/src/main/res/values/strings.xml')
    )


def test_get_module_type_github_workspace_returns_hidden():
    assert ModuleType.HIDDEN == get_module_type(get_change_data(GITHUB_WORKFLOW_PATH))
