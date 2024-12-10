"""Python Object JSON Tool pyobjson.json module.

Attributes:
    __author__ (str): Python package template author.
    __email__ (str): Python package template author email.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

from collections.abc import Collection, Callable
from inspect import getfullargspec
from typing import Dict, List, Any, Type
from pathlib import Path

from pyobjson.utils import clean_data_dict, derive_custom_class_key, derive_typed_key_value_pairs


def serialize(custom_class_instance: Any, pyobjson_base_custom_subclasses: List[Type]) -> Dict[str, Any]:
    """Recursive method to serialize custom Python objects into nested dictionaries for conversion to JSON.

    Args:
        custom_class_instance (Any): Custom Python class instance to serialize.
        pyobjson_base_custom_subclasses (list[Type]): List of custom Python class subclasses.

    Returns:
        dict[str, Any]: Serializable dictionary.

    """
    serializable_dict = dict()
    for att, val in clean_data_dict(custom_class_instance, pyobjson_base_custom_subclasses).items():
        if type(val) in pyobjson_base_custom_subclasses:
            serializable_dict[att] = serialize(val, pyobjson_base_custom_subclasses)
        elif isinstance(val, Collection) and not isinstance(val, (str, bytes, bytearray)):
            values = []
            for v in val:
                if type(v) in pyobjson_base_custom_subclasses:
                    values.append(serialize(v, pyobjson_base_custom_subclasses))
                else:
                    values.append(v)
            # TODO: handle serialization of specific classes like set so that they can be deserialized properly
            # serializable_dict[f"{type(val).__name__.lower()}.{att}"] = values
            serializable_dict[att] = values
        elif isinstance(val, Path):
            serializable_dict[f"path.{att}"] = str(val)
        elif isinstance(val, Callable):
            serializable_dict[f"callable.{att}"] = f"{val.__name__}:{','.join(getfullargspec(val).args)}"
        else:
            serializable_dict[att] = val
    return {derive_custom_class_key(custom_class_instance.__class__): serializable_dict}


def deserialize(json_data: Any, pyobjson_base_custom_subclasses_by_key: Dict[str, Type]) -> Any:
    """Recursive method to deserialize JSON into typed data structures for conversion to custom Python objects.

    Args:
        json_data (Any): JSON data to be deserialized.
        pyobjson_base_custom_subclasses_by_key (dict[str, Type]): Dictionary with snakecase strings of all subclasses of
            PythonObjectJson as keys and subclasses as values.

    Returns:
        obj (Any): Object deserialized from JSON.
    """
    base_subclasses: Dict[str, Type] = pyobjson_base_custom_subclasses_by_key

    # TODO: handle correct deserialization of specific serialized classes like set
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
                    for k, v in class_attributes.items()
                    if k in class_args
                }
            )

            # assign the remaining class attributes to the created class instance
            vars(class_instance).update(
                {k: deserialize(v, base_subclasses) for k, v in derive_typed_key_value_pairs(class_attributes).items()}
            )

            return class_instance
        else:
            return {k: deserialize(v, base_subclasses) for k, v in derive_typed_key_value_pairs(json_data).items()}
    else:
        return json_data
