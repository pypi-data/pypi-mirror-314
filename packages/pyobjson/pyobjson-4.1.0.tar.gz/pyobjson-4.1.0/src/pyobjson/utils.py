"""Python Object JSON Tool pyobjson.utils module.

Attributes:
    __author__ (str): Python package template author.
    __email__ (str): Python package template author email.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

from inspect import getfullargspec
from typing import Type, Callable, Union


def derive_custom_object_key(custom_object: Union[Type, Callable]) -> str:
    """Utility function to derive a key for a custom object representing the fully qualified name of that object.

    Args:
        custom_object (Type): The custom object for which to derive a key.

    Returns:
        str: The fully qualified name of the object in lowercase (e.g. module.submodule.object).

    """
    # avoid including module if no module exists or the object is in the Python builtins
    if (obj_module := getattr(custom_object, "__module__", None)) and obj_module != "builtins":
        return f"{obj_module.lower()}.{custom_object.__qualname__.lower()}"
    else:
        return custom_object.__qualname__.lower()


def derive_custom_callable_value(custom_callable: Callable) -> str:
    """Utility function to derive a string value from a custom callable object.

    Args:
        custom_callable (Callable): Custom callable object for which to derive a string representation value.

    Returns:
        str: A string representing the custom callable object that can be used to import and call that object.

    """
    arg_spec_str = ",".join([f"{k}:{v.__name__}" for k, v in getfullargspec(custom_callable).annotations.items()])
    return f"{derive_custom_object_key(custom_callable)}::{arg_spec_str}"
