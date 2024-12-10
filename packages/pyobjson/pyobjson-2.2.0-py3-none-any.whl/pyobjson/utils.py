"""Python Object JSON Tool pyobjson.utils module.

Attributes:
    __author__ (str): Python package template author.
    __email__ (str): Python package template author email.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

from pathlib import Path
from typing import Dict, Any, List, Type


def clean_data_dict(custom_class_instance: Any, pyobjson_base_custom_subclasses: List[Type]) -> Dict[str, Any]:
    """Recursive utility method to un-type custom class type objects for serialization.

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


def derive_typed_key_value_pairs(json_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Utility method to derive both keys and Python object types from specially formatted dictionary keys and make
    their respective values into Python objects of those types.

    Args:
        json_dict (Dict[str, Any]): JSON dictionary that may contain keys in the format type.key_name (e.g.
            path.root_directory) with corresponding string values representing Python objects of that type.

    Returns:
        dict[str, Any]: Dictionary with both keys and Python object values derived from specially formatted JSON
            dictionary keys.

    """
    derived_key_value_pairs = {}
    for key, value in json_dict.items():
        if key.count(".") == 1:
            type_str, key = key.split(".")

            if type_str == "path":  # handle posix paths
                value = Path(value)
            elif type_str == "callable":  # TODO: handle proper serialization and reconstruction of functions
                value = None

            derived_key_value_pairs[key] = value
        else:
            # add key-value pair without modification if key is not formatted with a single "." to indicate a value type
            derived_key_value_pairs[key] = value

    return derived_key_value_pairs
