"""Pytest top-level conftest.py.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Callable

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

    def __init__(self, child_class_dict: Dict[str, ChildClass], child_class_list: List[ChildClass],
                 parent_class_set: Optional[Set[str]], parent_class_tuple: Optional[Tuple[str]],
                 parent_class_file: Optional[Path], parent_class_external_function: Optional[Callable],
                 parent_class_datetime: Optional[datetime]):
        super().__init__()
        self.child_class_dict: Dict[str, ChildClass] = child_class_dict
        self.child_class_list: List[ChildClass] = child_class_list
        self.parent_class_set: Set[str] = parent_class_set
        self.parent_class_tuple: Tuple[str] = parent_class_tuple
        self.parent_class_file: Path = parent_class_file
        self.parent_class_external_function: Optional[Callable] = parent_class_external_function
        self.parent_class_datetime: datetime = parent_class_datetime


@fixture(scope="module")
def parent_class_with_nested_child_classes() -> ParentClass:
    """Create ParentClass instance for testing.

    Returns:
        ParentClass: Instance of ParentClass.
    """
    return ParentClass(
        {"child_class_1": ChildClass([ChildChildClass("test_child_child_class_argument_in_dict")])},
        [ChildClass([ChildChildClass("test_child_child_class_argument_in_list")])],
        {"test_parent_class_collection_element"},
        ("test_parent_class_collection_element",),
        Path(__name__),
        external_function,
        datetime(2024, 1, 1, 0, 0, 0)
    )


@fixture(scope="module")
def parent_class_json_str() -> str:
    """Create JSON string from ParentClass instance for testing.

    Returns:
        str: JSON string derived from serialized ParentClass instance.

    """
    return json.dumps(
        {
            "conftest.parentclass": {
                "collection:dict.child_class_dict": {
                    "child_class_1": {
                        "conftest.childclass": {
                            "collection:list.child_child_class_list": [
                                {
                                    "conftest.childchildclass": {
                                        "child_child_class_param": "test_child_child_class_argument_in_dict"
                                    }
                                }
                            ]
                        }
                    }
                },
                "collection:list.child_class_list": [
                    {
                        "conftest.childclass": {
                            "collection:list.child_child_class_list": [
                                {
                                    "conftest.childchildclass": {
                                        "child_child_class_param": "test_child_child_class_argument_in_list"
                                    }
                                }
                            ]
                        }
                    }
                ],
                "collection:set.parent_class_set": [
                    "test_parent_class_collection_element"
                ],
                "collection:tuple.parent_class_tuple": [
                    "test_parent_class_collection_element"
                ],
                "path.parent_class_file": "conftest",
                "callable.parent_class_external_function": (
                    "conftest.external_function::param1:str,param2:str"
                ),
                "datetime.parent_class_datetime": "2024-01-01T00:00:00"
            }
        },
        ensure_ascii=False,
        indent=2
    )
