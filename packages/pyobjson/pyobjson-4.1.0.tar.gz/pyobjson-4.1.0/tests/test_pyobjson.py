"""Pytest test for Python Object JSON Tool code.

Note:
    Tests pyobjson.base module.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from conftest import ParentClass, ChildClass, ChildChildClass


class TestPythonObjectJson:

    def test_serialization_to_json_string(self, parent_class_with_nested_child_classes, parent_class_json_str):
        assert parent_class_with_nested_child_classes.to_json_str() == parent_class_json_str

    def test_deserialization_from_json_string(self, parent_class_json_str):
        # create ParentClass instance with all empty/None arguments
        parent_class_instance = ParentClass(
            {},
            [],
            None,
            None,
            None,
            None,
            None,
            None
        )

        # check that all ParentClass attributes have no values
        assert not parent_class_instance.child_class_dict
        assert not parent_class_instance.child_class_list
        assert not parent_class_instance.parent_class_set
        assert not parent_class_instance.parent_class_tuple
        assert not parent_class_instance.parent_class_bytes
        assert not parent_class_instance.parent_class_file
        assert not parent_class_instance.parent_class_external_function
        assert not parent_class_instance.parent_class_datetime

        # load object instance from JSON string
        parent_class_instance.from_json_str(parent_class_json_str)

        # check that all ParentClass attributes have values based on the loaded JSON string
        assert len(parent_class_instance.child_class_dict) == 1
        assert isinstance(parent_class_instance.child_class_dict["child_class_1"], ChildClass)
        assert len(parent_class_instance.child_class_dict["child_class_1"].child_child_class_list) == 1

        assert len(parent_class_instance.child_class_list) == 1
        assert isinstance(parent_class_instance.child_class_list[0], ChildClass)

        assert len(parent_class_instance.child_class_list[0].child_child_class_list) == 1
        assert isinstance(parent_class_instance.child_class_list[0].child_child_class_list[0], ChildChildClass)

        assert isinstance(parent_class_instance.parent_class_set, set)
        assert len(parent_class_instance.parent_class_set) == 1
        assert len(parent_class_instance.parent_class_set.intersection({"test_parent_class_collection_element"})) == 1

        assert isinstance(parent_class_instance.parent_class_tuple, tuple)
        assert len(parent_class_instance.parent_class_tuple) == 1
        assert parent_class_instance.parent_class_tuple[0] == "test_parent_class_collection_element"

        assert isinstance(parent_class_instance.parent_class_bytes, bytes)
        assert parent_class_instance.parent_class_bytes == b"test_parent_class_collection_element"

        assert isinstance(parent_class_instance.parent_class_file, Path)
        assert str(parent_class_instance.parent_class_file) == "conftest"

        assert isinstance(parent_class_instance.parent_class_external_function, Callable)
        assert parent_class_instance.parent_class_external_function("hello", "world") == "hello.world"

        assert isinstance(parent_class_instance.parent_class_datetime, datetime)
        assert parent_class_instance.parent_class_datetime.isoformat() == "2024-01-01T00:00:00"
