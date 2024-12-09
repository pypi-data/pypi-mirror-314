""" Testing Main.
"""
from pathlib import Path
from unittest.mock import Mock
from xml.etree.ElementTree import ElementTree
import pytest


def test_main_simple_cl_xml(simple_changelist_xml):
    with pytest.MonkeyPatch().context() as ctx:
        import sys
        original_argv = sys.argv
        sys.argv = ['changelist_sort', '--workspace', 'testfile']
        # Now Import
        from changelist_sort.__main__ import main
        # Mock File Input
        ctx.setattr(Path, 'exists', lambda _: True)
        ctx.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        ctx.setattr(Path, 'stat', lambda _: obj)
        ctx.setattr(Path, 'read_text', lambda _: simple_changelist_xml)
        # Mock File Write
        def element_tree_write(
            self: ElementTree, file_or_filename, encoding='utf-8',
            xml_declaration=True, method='xml',
            default_namespace=None,
            short_empty_elements=True,
        ):
            global TAG
            global VERSION
            elem = self.getroot()
            TAG = elem.tag
            VERSION = elem.attrib['version']
        ctx.setattr(ElementTree, 'write', element_tree_write)
        # Run Main
        main()
        assert TAG == 'project'
        assert VERSION == '4'
        sys.argv = original_argv
