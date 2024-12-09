import pytest
from changelist_data.xml import workspace


@pytest.fixture()
def simple_workspace_tree(simple_changelist_xml):
    return workspace.load_xml(simple_changelist_xml)


@pytest.fixture()
def multi_workspace_tree(multi_changelist_xml):
    return workspace.load_xml(multi_changelist_xml)

