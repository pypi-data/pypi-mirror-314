"""Python Object JSON Tool pyobjson.json module.

Attributes:
    __author__ (str): Python package template author.
    __email__ (str): Python package template author email.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

from datetime import datetime
from importlib import import_module
from inspect import getfullargspec
from pathlib import Path
from typing import Dict, Any, Type, Callable
from typing import List

from pyobjson.utils import (
    derive_custom_object_key,
    derive_custom_callable_value,
)


def unpack_custom_class_vars(custom_class_instance: Any, pyobjson_base_custom_subclasses: List[Type]) -> Dict[str, Any]:
    """Recursive function to un-type custom class type objects for serialization.

    Args:
        custom_class_instance (Any): Custom Python class instance to be serialized.
        pyobjson_base_custom_subclasses (list[Type]): List of custom Python class subclasses.

    Returns:
        dict[str, Any]: Dictionary that extracts serializable data from custom objects.

    """
    clean_dict = {}
    for k, v in vars(custom_class_instance).items():
        clean_dict[k] = (
            unpack_custom_class_vars(v, pyobjson_base_custom_subclasses)
            if type(v) in pyobjson_base_custom_subclasses
            else v
        )
    return clean_dict


def extract_typed_key_value_pairs(json_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Function to extract both keys and Python object types from specially formatted dictionary keys and make their
    respective values into Python objects of those types.

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

            type_name, key = key.split(".")
            type_category = None
            if type_name.count(":") == 1:
                type_category, type_name = type_name.split(":")

            if type_category == "collection":
                if type_name == "dict":
                    # do nothing because dictionaries are supported in JSON
                    pass
                elif type_name == "list":
                    # do nothing because lists are supported in JSON
                    pass
                elif type_name == "set":
                    value = set(value)
                elif type_name == "tuple":
                    value = tuple(value)
            elif type_name == "path":  # handle posix paths
                value = Path(value)
            elif type_name == "callable":  # handle callables (functions, methods, etc.)
                # extract the callable components from a value with format module.callable::arg1:type1,arg2:type2
                callable_path, callable_args = value.split("::", 1)
                # extract the callable module and name
                module, callable_name = callable_path.rsplit(".", 1)
                # use the callable module and name to import the callable itself and set it to the value
                value = getattr(import_module(module), callable_name)
            elif type_name == "datetime":  # handle datetime objects
                value = datetime.fromisoformat(value)
            else:
                raise ValueError(f"JSON data ({key}: {value}) is not compatible with pyobjson.")

            derived_key_value_pairs[key] = value
        else:
            # add key-value pair without modification if key is not formatted with a single "." to indicate a value type
            derived_key_value_pairs[key] = value

    return derived_key_value_pairs


def serialize(custom_class_instance: Any, pyobjson_base_custom_subclasses: List[Type]) -> Dict[str, Any]:
    """Recursive function to serialize custom Python objects into nested dictionaries for conversion to JSON.

    Args:
        custom_class_instance (Any): Custom Python class instance to serialize.
        pyobjson_base_custom_subclasses (list[Type]): List of custom Python class subclasses.

    Returns:
        dict[str, Any]: Serializable dictionary.

    """
    serializable_dict = dict()
    for att, val in unpack_custom_class_vars(custom_class_instance, pyobjson_base_custom_subclasses).items():
        if type(val) in pyobjson_base_custom_subclasses:
            serializable_dict[att] = serialize(val, pyobjson_base_custom_subclasses)
        elif isinstance(val, dict):
            serializable_dict[f"collection:dict.{att}"] = {
                k: serialize(v, pyobjson_base_custom_subclasses)
                if type(v) in pyobjson_base_custom_subclasses
                else v
                for k, v in val.items()
            }
        elif isinstance(val, (list, set, tuple)):
            values = []
            for v in val:
                if type(v) in pyobjson_base_custom_subclasses:
                    values.append(serialize(v, pyobjson_base_custom_subclasses))
                else:
                    values.append(v)
            serializable_dict[f"collection:{derive_custom_object_key(val.__class__)}.{att}"] = values
        elif isinstance(val, Path):
            serializable_dict[f"path.{att}"] = str(val)
        elif isinstance(val, Callable):
            serializable_dict[f"callable.{att}"] = derive_custom_callable_value(val)
        elif isinstance(val, datetime):
            serializable_dict[f"datetime.{att}"] = val.isoformat()
        else:
            serializable_dict[att] = val
    return {derive_custom_object_key(custom_class_instance.__class__): serializable_dict}


def deserialize(json_data: Any, pyobjson_base_custom_subclasses_by_key: Dict[str, Type]) -> Any:
    """Recursive function to deserialize JSON into typed data structures for conversion to custom Python objects.

    Args:
        json_data (Any): JSON data to be deserialized.
        pyobjson_base_custom_subclasses_by_key (dict[str, Type]): Dictionary with snakecase strings of all subclasses of
            PythonObjectJson as keys and subclasses as values.

    Returns:
        obj (Any): Object deserialized from JSON.
    """
    base_subclasses: Dict[str, Type] = pyobjson_base_custom_subclasses_by_key
    if isinstance(json_data, list):  # recursively deserialize all elements if json_data is a list
        return [deserialize(item, base_subclasses) for item in json_data]
    elif isinstance(json_data, dict):  # recursively deserialize all values if json_data is a dictionary
        # noinspection PyUnboundLocalVariable
        if len(json_data) == 1 and (single_key := next(iter(json_data.keys()))) and single_key in base_subclasses:
            # check if json_data is a dict with only one key that matches a custom subclass for object derivation

            # noinspection PyPep8Naming
            ClassObject = base_subclasses[single_key]  # retrieve custom subclass
            class_args = getfullargspec(ClassObject.__init__).args[1:]  # get __init__ arguments for custom subclass
            class_attributes: Dict[str, Any] = json_data[single_key]  # get JSON to be deserialized

            # create an instance of the custom subclass using the __init__ arguments
            class_instance = ClassObject(
                **{
                    k: deserialize(v, base_subclasses)
                    for k, v in extract_typed_key_value_pairs(class_attributes).items()
                    if k in class_args
                }
            )

            # assign the remaining class attributes to the created class instance
            vars(class_instance).update(
                {k: deserialize(v, base_subclasses) for k, v in extract_typed_key_value_pairs(class_attributes).items()}
            )

            return class_instance
        else:
            return {k: deserialize(v, base_subclasses) for k, v in extract_typed_key_value_pairs(json_data).items()}
    else:
        return json_data
