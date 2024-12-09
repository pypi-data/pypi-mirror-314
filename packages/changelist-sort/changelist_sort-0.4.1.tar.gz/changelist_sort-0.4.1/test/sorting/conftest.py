import pytest

from changelist_sort import list_key
from changelist_sort.list_key import ListKey, compute_key
from changelist_sort.sorting import SortingChangelist
from changelist_sort.sorting.module_type import ModuleType
from changelist_sort.sorting.sorting_file_pattern import SortingFilePattern


@pytest.fixture
def shell_scripts_file_pattern() -> SortingFilePattern:
    return SortingFilePattern(file_ext='sh')


@pytest.fixture
def shell_scripts_changelist(shell_scripts_file_pattern) -> SortingChangelist:
    return SortingChangelist(
        module_type=ModuleType.ROOT,
        list_key=ListKey(key='shellscripts', changelist_name='Shell Scripts'),
        file_patterns=[shell_scripts_file_pattern],
    )


@pytest.fixture
def sort_config_empty() -> SortingChangelist:
    return SortingChangelist(
        module_type=None,
        list_key=compute_key(''),
        file_patterns=[],
    )


@pytest.fixture
def sort_config_all() -> SortingChangelist:
    return SortingChangelist(
        module_type=None,
        list_key=compute_key('all'),
        file_patterns=[
            SortingFilePattern(inverse=True)
        ],
    )


@pytest.fixture
def sorting_cl_root_markdown_docs() -> SortingChangelist:
    return SortingChangelist(
        module_type=ModuleType.ROOT,
        list_key=compute_key('Documentation'),
        file_patterns=[
            SortingFilePattern(file_ext='md'),
        ],
    )


@pytest.fixture
def sorting_cl_any_markdown_docs() -> SortingChangelist:
    return SortingChangelist(
        module_type=None,
        list_key=compute_key('Documentation'),
        file_patterns=[
            SortingFilePattern(file_ext='md'),
        ],
    )


@pytest.fixture
def sort_config_github_workflows_yml() -> list[SortingChangelist]:
    return [
        SortingChangelist(
            module_type=None,
            list_key=ListKey('githubworkflows', 'GitHub Workflows'),
            file_patterns=[
                SortingFilePattern(first_dir='.github'),
                SortingFilePattern(path_end='workflows'),
                SortingFilePattern(path_end='workflows/'),
                SortingFilePattern(file_ext='yml'),
            ],
        ),
    ]


@pytest.fixture
def sort_config_github_workflows_yml_2() -> list[SortingChangelist]:
    return [
        SortingChangelist(
            module_type=ModuleType.HIDDEN,
            list_key=compute_key('github_workflows'),
            file_patterns=[
                SortingFilePattern(path_start='.github/workflows/'),
                SortingFilePattern(path_start='.github/workflows'),
                SortingFilePattern(path_start='/.github/workflows'),
                SortingFilePattern(file_ext='.yml'),
            ],
        ),
    ]


@pytest.fixture
def sort_config_python_test_files() -> list[SortingChangelist]:
    return [
        SortingChangelist(
            module_type=ModuleType.MODULE,
            list_key=compute_key('Test Files'),
            file_patterns=[
                SortingFilePattern(filename_prefix='test'),
                SortingFilePattern(file_ext='py'),
            ],
        ),
    ]


@pytest.fixture
def sort_config_python_reader_files() -> list[SortingChangelist]:
    """ Matches Python files with names ending "reader".
    """
    return [
        SortingChangelist(
            module_type=ModuleType.MODULE,
            list_key=compute_key('Python Reader Files'),
            file_patterns=[
                SortingFilePattern(filename_suffix='reader'),
                SortingFilePattern(file_ext='py'),
            ],
        ),
    ]


SRC_DIR_PATTERN = SortingFilePattern(first_dir='changelist_sort')
TEST_DIR_PATTERN = SortingFilePattern(first_dir='test')
INPUT_PACKAGE_PATTERN = SortingFilePattern(path_end='input')
SORTING_PACKAGE_PATTERN = SortingFilePattern(path_end='sorting')
WORKSPACE_PACKAGE_PATTERN = SortingFilePattern(path_end='workspace')

BUILD_UPDATES_KEY = list_key.compute_key('Build Updates')


@pytest.fixture
def sorting_cl_input_package_tests():
    return SortingChangelist(
        list_key.compute_key('Input Package Tests'),
        [
            TEST_DIR_PATTERN,
            INPUT_PACKAGE_PATTERN,
        ],
        ModuleType.MODULE,
    )


@pytest.fixture
def sorting_cl_input_package():
    return SortingChangelist(
        list_key.compute_key('Input Package'),
        [
            SRC_DIR_PATTERN,
            INPUT_PACKAGE_PATTERN,
        ],
        ModuleType.MODULE,
    )


@pytest.fixture
def sorting_cl_all_files_in_tests():
    """ All Files in the 'test' Directory.
    """
    return SortingChangelist(
        list_key.compute_key('Tests'),
        [
            TEST_DIR_PATTERN,
        ],
        ModuleType.MODULE,
    )


@pytest.fixture
def sorting_cl_pytest_files():
    """ Pytest Files: 'test_*.py' files in the 'test' Directory.
    """
    return SortingChangelist(
        list_key.compute_key('Pytest Modules'),
        [
            TEST_DIR_PATTERN,
            SortingFilePattern(filename_prefix='test_'),
            SortingFilePattern(file_ext='py'),
        ],
        ModuleType.MODULE,
    )


@pytest.fixture
def sorting_cl_src_package():
    """ """
    return SortingChangelist(
        list_key.compute_key('Main Package Source'),
        [
            SRC_DIR_PATTERN,
        ],
        ModuleType.MODULE,
    )


@pytest.fixture
def sort_config_developer_cl_0(
    sorting_cl_input_package_tests,
    sorting_cl_input_package,
    sorting_cl_any_markdown_docs,
    sorting_cl_all_files_in_tests,
    sorting_cl_src_package,
    shell_scripts_changelist,
):
    return (
        sorting_cl_any_markdown_docs,
        sorting_cl_input_package,
        sorting_cl_input_package_tests,
        SortingChangelist(
            list_key.compute_key('Sorting Package Tests'),
            [
                TEST_DIR_PATTERN,
                SORTING_PACKAGE_PATTERN,
            ],
            ModuleType.MODULE,
        ),
        SortingChangelist(
            list_key.compute_key('Workspace Package Tests'),
            [
                TEST_DIR_PATTERN,
                WORKSPACE_PACKAGE_PATTERN,
            ],
            ModuleType.MODULE,
        ),
        sorting_cl_all_files_in_tests,  # Tests that don't match a pattern
        SortingChangelist(
            list_key.compute_key('Sorting Package'),
            [
                SRC_DIR_PATTERN,
                SORTING_PACKAGE_PATTERN,
            ],
            ModuleType.MODULE,
        ),
        SortingChangelist(
            list_key.compute_key('Workspace Package'),
            [
                SRC_DIR_PATTERN,
                WORKSPACE_PACKAGE_PATTERN,
            ],
            ModuleType.MODULE,
        ),
        sorting_cl_src_package,
        shell_scripts_changelist,
        SortingChangelist(
            list_key.compute_key('Project Root'),
            [
                SortingFilePattern(
                    inverse=True,
                    first_dir='gradle',
                ),
                SortingFilePattern(
                    inverse=True,
                    file_ext='gradle',
                ),
                SortingFilePattern(
                    inverse=True,
                    file_ext='kts',
                ),
            ],
            ModuleType.ROOT,
        ),
        SortingChangelist(
            BUILD_UPDATES_KEY,
            [
                SortingFilePattern(
                    inverse=True,
                    first_dir='gradle',
                ),
                SortingFilePattern(
                    inverse=True,
                    first_dir='',
                ),
            ],
            ModuleType.GRADLE,
        ),
        SortingChangelist(
            BUILD_UPDATES_KEY,
            [
                SortingFilePattern(file_ext='gradle'),
            ],
            ModuleType.ROOT,
        ),
        SortingChangelist(
            BUILD_UPDATES_KEY,
            [
                SortingFilePattern(file_ext='properties'),
            ],
            ModuleType.ROOT,
        ),
        SortingChangelist(
            list_key.compute_key('Module Gradle Build Files'),
            [
                SortingFilePattern(
                    inverse=True,
                    first_dir='gradle',
                ),
                SortingFilePattern(
                    inverse=True,
                    first_dir='',
                ),
            ],
            ModuleType.GRADLE,
        )
    )
