import pytest

from changelist_sort.list_key import ListKey
from changelist_sort.sorting.sorting_changelist import SortingChangelist
from changelist_sort.sorting.sorting_file_pattern import SortingFilePattern
from changelist_sort.sorting.module_type import ModuleType


@pytest.fixture
def sorting_xml_sample_1():
    return """<?xml version='1.0' encoding='utf-8'?>
<sorting>
    <changelist key="root" name="Project Root Python Files" module="root">
        <files path_end=".py"></files>
    </changelist>
</sorting>"""


@pytest.fixture
def sorting_xml_sample_2():
    return """<?xml version='1.0' encoding='utf-8'?>
<sorting>
    <changelist key="source" name="Source Files">
        <files file_ext=".py" />
    </changelist>
    <changelist key="text" name="Text Files">
        <files file_ext=".txt" />
    </changelist>
    <changelist key="test" name="Tests">
        <files first_dir="test" />
    </changelist>
</sorting>"""


@pytest.fixture
def sorting_xml_sample_3():
    return """<sorting>
    <changelist key="github" name="GitHub Actions CI" module="hidden">
        <files filename_prefix="ci" />
        <files file_ext="yml" />
    </changelist>
    <changelist key="dependabot" name="GitHub Dependabot" module="hidden">
        <files filename_prefix="dependabot" />
    </changelist>
</sorting>"""


@pytest.fixture
def sorting_xml_sample_4():
    return """<sorting>
    <changelist key="app" name="App Module Source Files" module="module">
        <files file_ext="kt" />
    </changelist>
    <changelist key="app" name="App Module Source Files" module="module">
        <files file_ext="java" />
    </changelist>
    <changelist key="gradle" name="Gradle Build Files" module="gradle">
        <files inverse="true" />
    </changelist>
</sorting>"""


@pytest.fixture
def sorting_config_list_sample1():
    return [
        SortingChangelist(
            list_key=ListKey('root', 'Project Root Python Files'),
            file_patterns=[
                SortingFilePattern(
                    path_end='.py',
                ),
            ],
            module_type=ModuleType.ROOT,
        ),
    ]


@pytest.fixture
def sorting_config_list_sample2():
    return [
        SortingChangelist(
            list_key=ListKey('source', 'Source Files'),
            file_patterns=[
                SortingFilePattern(file_ext='.py')
            ],
        ),
        SortingChangelist(
            list_key=ListKey('text', 'Text Files'),
            file_patterns=[
                SortingFilePattern(file_ext='.txt')
            ],
        ),
        SortingChangelist(
            list_key=ListKey('test', 'Tests'),
            file_patterns=[
                SortingFilePattern(first_dir='test')
            ],
        ),
    ]


@pytest.fixture
def sorting_config_list_sample3():
    return [
        SortingChangelist(
            list_key=ListKey("github", "GitHub Actions CI"),
            file_patterns=[
                SortingFilePattern(filename_prefix='ci'),
                SortingFilePattern(file_ext='yml'),
            ],
            module_type=ModuleType.HIDDEN,
        ),
        SortingChangelist(
            list_key=ListKey("dependabot", "GitHub Dependabot"),
            file_patterns=[
                SortingFilePattern(filename_prefix='dependabot'),
            ],
            module_type=ModuleType.HIDDEN,
        ),
    ]


@pytest.fixture
def sorting_config_list_sample4():
    return [
        SortingChangelist(
            list_key=ListKey("app", "App Module Source Files"),
            file_patterns=[
                SortingFilePattern(file_ext='kt'),
            ],
            module_type=ModuleType.MODULE,
        ),
        SortingChangelist(
            list_key=ListKey("app", "App Module Source Files"),
            file_patterns=[
                SortingFilePattern(file_ext='java'),
            ],
            module_type=ModuleType.MODULE,
        ),
        SortingChangelist(
            list_key=ListKey("gradle", "Gradle Build Files"),
            file_patterns=[
                SortingFilePattern(inverse=True),
            ],
            module_type=ModuleType.GRADLE,
        ),
    ]
