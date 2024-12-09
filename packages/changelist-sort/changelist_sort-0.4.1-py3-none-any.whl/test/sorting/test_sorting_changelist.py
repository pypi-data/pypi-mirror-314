""" Testing Developer Changelist
"""
from changelist_sort import list_key
from changelist_sort.sorting.file_sort import get_module_type
from changelist_sort.sorting.module_type import ModuleType
from changelist_sort.sorting.sorting_changelist import SortingChangelist, filter_by_module

from test.conftest import get_change_data
from test.sorting.conftest import INPUT_PACKAGE_PATTERN, SRC_DIR_PATTERN


def get_dc_src_input() -> SortingChangelist:
    return SortingChangelist(
        list_key.compute_key('Input Source Package'),
        [
            SRC_DIR_PATTERN,
            INPUT_PACKAGE_PATTERN
        ]
    )


def test_check_file_src_dir_input_pattern_input_data_returns_true():
    instance = get_dc_src_input()
    assert instance.check_file(get_change_data('/changelist_sort/input/input_data.py'))
    

def test_check_file_src_dir_input_pattern_init_file_returns_false():
    instance = get_dc_src_input()
    assert not instance.check_file(get_change_data('/changelist_sort/__init__.py'))


def test_check_file_root_markdown_docs_with_root_readme_cd_returns_true(
        sorting_cl_root_markdown_docs,
    root_readme_change_data
):
    assert sorting_cl_root_markdown_docs.check_file(root_readme_change_data)


def test_check_file_python_reader_files_with_python_reader_cd_returns_true(
    sort_config_python_reader_files,
    python_reader_cd
):
    assert sort_config_python_reader_files[0].check_file(python_reader_cd)


def test_check_file_python_reader_files_with_module_src_cd_returns_false(
    sort_config_python_reader_files,
    module_src_change_data
):
    assert not sort_config_python_reader_files[0].check_file(module_src_change_data)


def test_check_file_python_test_files_with_python_test_cd_returns_true(
    sort_config_python_test_files,
    python_test_cd
):
    assert sort_config_python_test_files[0].check_file(python_test_cd)


def test_check_file_python_test_files_with_module_test_cd_returns_false(
    sort_config_python_test_files,
    module_test_change_data
):
    assert not sort_config_python_test_files[0].check_file(module_test_change_data)


def test_check_file_gh_workflows_with_gh_workflow_cd_returns_true(
    sort_config_github_workflows_yml,
    github_workflows_change_data
):
    assert sort_config_github_workflows_yml[0].check_file(github_workflows_change_data)


def test_check_file_gh_workflows2_with_gh_workflow_cd_returns_true(
    sort_config_github_workflows_yml_2,
    github_workflows_change_data
):
    assert sort_config_github_workflows_yml_2[0].check_file(github_workflows_change_data)


def test_check_file_gh_workflows_with_markdown_cd_returns_false(
    sort_config_github_workflows_yml,
    dependabot_change_data
):
    assert not sort_config_github_workflows_yml[0].check_file(dependabot_change_data)


def test_check_file_gh_workflows2_with_gh_workflow_cd_returns_false(
    sort_config_github_workflows_yml_2,
    dependabot_change_data
):
    assert not sort_config_github_workflows_yml_2[0].check_file(dependabot_change_data)


def test_check_file_empty_config_with_python_reader_cd_returns_false(
    sort_config_empty,
    python_reader_cd
):
    assert not sort_config_empty.check_file(python_reader_cd)


def test_check_file_empty_config_with_root_readme_cd_returns_false(
    sort_config_empty,
    root_readme_change_data
):
    assert not sort_config_empty.check_file(root_readme_change_data)


def test_check_file_empty_config_with_gh_workflows_cd_returns_false(
    sort_config_empty,
    github_workflows_change_data
):
    assert not sort_config_empty.check_file(github_workflows_change_data)


def test_check_file_all_config_with_python_reader_returns_true(
    sort_config_all,
    python_reader_cd
):
    assert sort_config_all.check_file(python_reader_cd)


def test_check_file_all_config_with_root_readme_cd_returns_true(
    sort_config_all,
    root_readme_change_data
):
    assert sort_config_all.check_file(root_readme_change_data)


def test_check_file_all_config_with_gh_workflows_cd_returns_true(
    sort_config_all,
    github_workflows_change_data
):
    assert sort_config_all.check_file(github_workflows_change_data)


def test_filter_patterns_by_module_none_returns_only_none(sort_config_developer_cl_0):
    result = filter_by_module(None, sort_config_developer_cl_0)
    assert len(result) == 1
    assert result[0].module_type is None


def test_filter_patterns_by_module_root_returns_tuple(sort_config_developer_cl_0):
    result = filter_by_module(ModuleType.ROOT, sort_config_developer_cl_0)
    assert len(result) == 5
    for x in result:
        assert x.module_type == ModuleType.ROOT or x.module_type is None

def test_filter_patterns_by_module_gradle_returns_tuple(sort_config_developer_cl_0):
    result = filter_by_module(ModuleType.GRADLE, sort_config_developer_cl_0)
    assert len(result) == 3
    for x in result:
        assert x.module_type == ModuleType.GRADLE or x.module_type is None


def test_filter_patterns_by_module_module_returns_tuple(sort_config_developer_cl_0):
    result = filter_by_module(ModuleType.MODULE, sort_config_developer_cl_0)
    assert len(result) == 9
    for x in result:
        assert x.module_type == ModuleType.MODULE or x.module_type is None


def test_filter_patterns_by_module_hidden_returns_tuple(sort_config_developer_cl_0):
    result = filter_by_module(ModuleType.HIDDEN, sort_config_developer_cl_0)
    assert len(result) == 1
    for x in result:
        assert x.module_type == ModuleType.HIDDEN or x.module_type is None


def test_filter_patterns_by_module_developer_cl_0_with_module_src_cd_returns_9_patterns(
    module_src_change_data,
    sort_config_developer_cl_0
):
    result = filter_by_module(
        get_module_type(module_src_change_data),
        sort_config_developer_cl_0
    )
    assert len(result) == 9 # The Number of Patterns with the given ModuleType
    for x in result:
        assert x.module_type == ModuleType.MODULE or x.module_type is None
