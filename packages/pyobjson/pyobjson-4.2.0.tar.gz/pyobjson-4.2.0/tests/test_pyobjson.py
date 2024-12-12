"""Pytest test for Python Object JSON Tool code.

Note:
    Tests pyobjson.base module.

"""

__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"


from conftest import ParentClass


class TestPythonObjectJson:
    def test_serialization_to_json_string(self, parent_class_with_nested_child_classes, parent_class_json_str):
        # confirm conftest.ParentClass instance as a JSON string is equal to the conftest ParentClass JSON string
        assert parent_class_with_nested_child_classes.to_json_str() == parent_class_json_str

    def test_deserialization_from_json_string(self, parent_class_with_nested_child_classes, parent_class_json_str):
        # create new ParentClass instance with all empty/None arguments
        parent_class_instance = ParentClass({}, [], None, None, None, None, None, None)

        # confirm new empty ParentClass instance is not equivalent to conftest.ParentClass instance
        assert parent_class_instance != parent_class_with_nested_child_classes

        # load conftest ParentClass JSON string to new empty ParentClass instance
        parent_class_instance.from_json_str(parent_class_json_str)

        # confirm newly created ParentClass instance loaded from JSON is equivalent to conftest.ParentClass instance
        assert parent_class_instance == parent_class_with_nested_child_classes
