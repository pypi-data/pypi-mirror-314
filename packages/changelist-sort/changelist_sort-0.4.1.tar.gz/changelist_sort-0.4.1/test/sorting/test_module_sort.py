""" Testing Module Sort Methods.
"""
import pytest

from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.sorting import file_sort
from changelist_sort.sorting import module_sort
from changelist_sort.sorting.module_sort import sort_file_by_module, is_sorted_by_module
from changelist_sort.sorting.module_type import ModuleType

from test.conftest import MODULE_SRC_PATH, get_change_data


@pytest.mark.parametrize(
    'key', [ModuleType.MODULE, ModuleType.HIDDEN]
)
def test_get_module_keys_user_modules(key):
    result = module_sort.get_module_keys(key)
    assert result == tuple()


def test_sort_file_by_module_empty_map_empty_file_returns_false():
    cl_map = ChangelistMap()
    empty_file = ChangeData()
    assert not sort_file_by_module(cl_map, empty_file)


def test_sort_file_by_module_empty_map_module_src_file_returns_true():
    cl_map = ChangelistMap()
    src_file = get_change_data(
        MODULE_SRC_PATH,
    )
    assert sort_file_by_module(cl_map, src_file)
    # Check CL Map for new Changelist
    new_cl = cl_map.search('module')
    assert new_cl is not None
    assert new_cl.name == 'Module'


def test_sort_file_by_module_app_gradle_file_returns_true_inserts_build_updates(
    app_gradle_build_change_data
):
    cl_map = ChangelistMap()
    assert sort_file_by_module(cl_map, app_gradle_build_change_data)
    # Check CL Map for new Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    new_cl = result[0]
    assert len(new_cl.changes) == 1
    assert new_cl.name == 'Build Updates'


def test_sort_file_by_module_gradle_properties_returns_true_inserts_build_updates(
    app_gradle_build_change_data
):
    cl_map = ChangelistMap()
    assert sort_file_by_module(cl_map, app_gradle_build_change_data)
    # Check CL Map for new Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    new_cl = result[0]
    assert len(new_cl.changes) == 1
    assert new_cl.name == 'Build Updates'


def test_sort_file_by_module_github_workflows_returns_true_inserts_github(
    github_workflows_change_data
):
    cl_map = ChangelistMap()
    assert sort_file_by_module(cl_map, github_workflows_change_data)
    # Check CL Map for new Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    new_cl = result[0]
    assert len(new_cl.changes) == 1
    assert new_cl.name == 'Github'


def test_sort_file_by_module_empty_file_returns_false():
    assert not sort_file_by_module(ChangelistMap(), ChangeData())


def test_sort_file_by_module_app_cl_app_gradle_returns_true(
    app_changelist,
    app_gradle_build_change_data
):
    cl_map = ChangelistMap()
    cl_map.insert(app_changelist)
    assert sort_file_by_module(cl_map, app_gradle_build_change_data)
    # A new Changelist is created called Build Updates
    result = cl_map.get_lists()
    assert len(result) == 2
    cl_0 = result[0]
    assert cl_0.name == 'App'
    cl_1 = result[1]
    assert cl_1.name == 'Build Updates'
    assert app_gradle_build_change_data in cl_1.changes


def test_sort_file_by_module_build_updates_cl_app_gradle_returns_true(
    build_updates_changelist,
    app_gradle_build_change_data
):
    cl_map = ChangelistMap()
    cl_map.insert(build_updates_changelist)
    assert sort_file_by_module(cl_map, app_gradle_build_change_data)
    # The Build Updates Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    assert result[0].name == 'Build Updates'


def test_sort_file_by_module_root_cl_readme_returns_true(
    root_changelist,
    root_readme_change_data
):
    cl_map = ChangelistMap()
    cl_map.insert(root_changelist)
    assert sort_file_by_module(cl_map, root_readme_change_data)
    # The Build Updates Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    assert result[0].name == 'Root'
    assert len(result[0].changes) == 1


def test_sort_file_by_module_module_cl_module_src_returns_true(
    module_changelist,
    module_src_change_data
):
    cl_map = ChangelistMap()
    cl_map.insert(module_changelist)
    assert sort_file_by_module(cl_map, module_src_change_data)
    # The Src file is added to the existing changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    cl_0 = result[0]
    assert cl_0.name == 'Module'
    assert module_src_change_data in cl_0.changes


def test_sort_file_by_module_zero_len_module_returns_false():
    new_cd = get_change_data('//hello.py')
    assert not sort_file_by_module(None, new_cd)


def test_sort_file_by_module_root_readme_returns_true(
    root_readme_change_data
):
    cl_map = ChangelistMap()
    assert file_sort.get_module_type(root_readme_change_data) == ModuleType.ROOT
    assert sort_file_by_module(cl_map, root_readme_change_data)


def test_is_sorted_by_module_module_cl(module_changelist):
    for file in module_changelist.changes:
        assert is_sorted_by_module(module_changelist.list_key, file)


def test_is_sorted_by_module_app_cl_app_gradle_returns_false(
    app_changelist,
    app_gradle_build_change_data
):
    assert not is_sorted_by_module(
        app_changelist.list_key, app_gradle_build_change_data
    )


def test_is_sorted_by_module_app_cl_strings_res_returns_true(
    app_changelist
):
    assert is_sorted_by_module(
        app_changelist.list_key, get_change_data('/app/src/main/res/values/strings.xml')
    )


def test_is_sorted_by_module_app_cl_src_file_returns_true(
    app_changelist
):
    assert is_sorted_by_module(
        app_changelist.list_key, get_change_data('/app/src/main/java/app/Main.java')
    )


def test_is_sorted_by_module_build_updates_cl_returns_true(
    build_updates_changelist
):
    cl = build_updates_changelist
    for file in cl.changes:
        assert is_sorted_by_module(cl.list_key, file)


def test_is_sorted_by_module_build_updates_cl_gradle_properties_returns_true(
    build_updates_changelist,
    gradle_properties_change_data
):
    assert is_sorted_by_module(
        build_updates_changelist.list_key, gradle_properties_change_data
    )


def test_is_sorted_by_module_github_cl(
    github_changelist
):
    assert is_sorted_by_module(
        github_changelist.list_key, get_change_data('/.github/workflow/test.yml')
    )


def test_is_sorted_by_module_github_cl_dependabot_returns_true(
    github_changelist
):
    assert is_sorted_by_module(
        github_changelist.list_key, get_change_data('/.github/dependabot.yml')
    )

def test_is_sorted_by_module_root_cl_gradlew_no_file_ext_returns_true(
    root_changelist
):
    assert is_sorted_by_module(
        root_changelist.list_key, get_change_data('/gradlew')
    )

def test_is_sorted_by_module_build_updates_cl_gradlew_no_file_ext_returns_false(
    build_updates_changelist
):
    assert not is_sorted_by_module(
        build_updates_changelist.list_key, get_change_data('/gradlew')
    )
