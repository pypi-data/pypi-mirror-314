"""Pytest test for Python Object JSON Tool code.

Note:
    Tests pyobjson.base module.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

from conftest import ParentClass


class TestPythonObjectJson:

    def test_serialization_to_json_string(self, parent_class_with_nested_child_classes, parent_class_json_str):
        assert parent_class_with_nested_child_classes.to_json_str() == parent_class_json_str

    def test_deserialization_from_json_string(self, parent_class_json_str):
        parent_class_instance = ParentClass([])
        assert not parent_class_instance.child_class_list

        parent_class_instance.from_json_str(parent_class_json_str)
        assert len(parent_class_instance.child_class_list) == 1
        assert len(parent_class_instance.child_class_list[0].child_child_class_list) == 1
