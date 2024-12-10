"""Python Object JSON Tool pyobjson.utils module.

Attributes:
    __author__ (str): Python package template author.
    __email__ (str): Python package template author email.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

from typing import Dict, Any, List, Type


def clean_data_dict(custom_class_instance: Any, pyobjson_base_custom_subclasses: List[Type]) -> Dict[str, Any]:
    """Recursive method to un-type custom class type objects for serialization.

    Args:
        custom_class_instance (Any): Custom Python class instance to be serialized.
        pyobjson_base_custom_subclasses (list[Type]): List of custom Python class subclasses.

    Returns:
        dict[str, Any]: Dictionary that extracts serializable data from custom objects.

    """
    clean_dict = {}
    for k, v in vars(custom_class_instance).items():
        clean_dict[k] = (
            clean_data_dict(v, pyobjson_base_custom_subclasses)
            if type(v) in pyobjson_base_custom_subclasses
            else v
        )
    return clean_dict


def derive_custom_class_key(custom_class: Type) -> str:
    """Utility method to derive a key for a custom class representing the fully qualified name of that class.

    Args:
        custom_class (Type): The custom class object for which to derive a key.

    Returns:
        str: The fully qualified name of the class in lowercase (e.g. module.submodule.class).
    """
    # avoid including module if no module exists or the class is in the Python builtins
    if (cls_module := getattr(custom_class, "__module__", None)) and cls_module != "builtins":
        return f"{cls_module.lower()}.{custom_class.__qualname__.lower()}"
    else:
        return custom_class.__qualname__.lower()
