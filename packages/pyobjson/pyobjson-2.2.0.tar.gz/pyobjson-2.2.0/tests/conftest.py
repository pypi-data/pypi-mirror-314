"""Pytest top-level conftest.py.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

import json
from pathlib import Path
from typing import List, Optional, Callable

from pytest import fixture

from pyobjson.base import PythonObjectJson


def external_function(param1: str, param2: str):
    return f"{param1}.{param2}"


class ChildChildClass(PythonObjectJson):
    """ChildChildClass for testing.
    """

    def __init__(self, child_child_class_param: str):
        super().__init__()
        self.child_child_class_param: str = child_child_class_param


class ChildClass(PythonObjectJson):
    """ChildClass for testing.
    """

    def __init__(self, child_child_class_list: List[ChildChildClass]):
        super().__init__()
        self.child_child_class_list: List[ChildChildClass] = child_child_class_list


class ParentClass(PythonObjectJson):
    """ParentClass for testing.
    """

    def __init__(self, child_class_list: List[ChildClass]):
        super().__init__()
        self.parent_class_file: Path = Path(__name__)
        self.parent_class_external_function: Optional[Callable] = external_function
        self.child_class_list: List[ChildClass] = child_class_list


@fixture(scope="module")
def parent_class_with_nested_child_classes() -> ParentClass:
    """Create ParentClass instance for testing.

    Returns:
        ParentClass: Instance of ParentClass.
    """
    return ParentClass([ChildClass([ChildChildClass("test_child_child_class_argument")])])


@fixture(scope="module")
def parent_class_json_str() -> str:
    """Create JSON string from ParentClass instance for testing.

    Returns:
        str: JSON string derived from serialized ParentClass instance.

    """
    return json.dumps(
        {
            "conftest.parentclass": {
                "path.parent_class_file": "conftest",
                "callable.parent_class_external_function": "external_function:param1,param2",
                "child_class_list": [
                    {
                        "conftest.childclass": {
                            "child_child_class_list": [
                                {
                                    "conftest.childchildclass": {
                                        "child_child_class_param": "test_child_child_class_argument"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        },
        ensure_ascii=False,
        indent=2
    )
