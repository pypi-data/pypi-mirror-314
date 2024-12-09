import pytest

from changelist_data.storage import ChangelistDataStorage
from changelist_data.xml import workspace
from changelist_data.xml.changelists import new_tree

from test.conftest import wrap_tree_in_storage


def create_storage(tree = new_tree()) -> ChangelistDataStorage:
    return wrap_tree_in_storage(tree)


@pytest.fixture()
def simple_storage(simple_changelist_xml):
    return wrap_tree_in_storage(workspace.read_xml(simple_changelist_xml))


@pytest.fixture()
def multi_storage(multi_changelist_xml):
    return wrap_tree_in_storage(workspace.read_xml(multi_changelist_xml))


@pytest.fixture
def no_changelist_xml() -> str:
    """No ChangelistManager Tag Workspace XML"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="AutoImportSettings">
    <option name="autoReloadType" value="NONE" />
  </component>
</project>"""


@pytest.fixture
def invalid_component_xml() -> str:
    """Invalid Workspace XML"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component>
  </component>
  <component name="ChangeListManager">
    <list default="true" id="af84ea1b-1b24-407d-970f-9f3a2835e933" name="Main" comment="Main Files">
      <change beforePath="$PROJECT_DIR$/main.py" beforeDir="false" />
    </list>
  </component>
</project>"""


@pytest.fixture
def get_cl_simple_xml() -> str:
    """Simple Changelists XML"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<changelists>
<list id="9f60fda2f83a47c88" name="Simple" comment="Main Program Files">
  <change beforePath="/main.py" beforeDir="false"  afterPath="/main.py" afterDir="false" />
</list>
</changelists>"""


@pytest.fixture
def get_cl_multi_xml() -> str:
    """Multi Changelists XML"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<changelists>
<list default="true" id="af84ea1b9f3a2835e933" name="Main" comment="Main Program Files">
  <change beforePath="/history.py" beforeDir="false" />
  <change beforePath="/main.py" beforeDir="false" />
</list>
<list id="9f60fda24c8f83a47c88" name="Test" comment="Test Files">
  <change afterPath="/test/test_file.py" afterDir="false" />
</list>
</changelists>"""
