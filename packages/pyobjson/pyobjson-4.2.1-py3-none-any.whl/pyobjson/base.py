"""Python Object JSON Tool pyobjson.base module.

Attributes:
    __author__ (str): Python package template author.
    __email__ (str): Python package template author email.

"""

__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

import json
from pathlib import Path
from typing import Any, Dict, Type

from pyobjson.data import deserialize, serialize
from pyobjson.utils import derive_custom_object_key


class PythonObjectJson(object):
    """Base Python Object with JSON serialization and deserialization compatibility."""

    def __init__(self, **kwargs):
        """Instantiate the PythonObjectJson class with all keyword arguments.

        Args:
            kwargs (dict): Key/value pairs to be passed to the PythonObjectJson class.

        """
        vars(self).update(kwargs)

    def __str__(self):
        return self.to_json_str()

    def __repr__(self):
        return (
            f"{derive_custom_object_key(self.__class__, as_lower=False)}"
            f"({','.join([f'{k}={v}' for k, v in vars(self).items()])})"
        )

    def __eq__(self, other):
        return type(self) is type(other) and vars(self) == vars(other)

    def _base_subclasses(self) -> Dict[str, Type]:
        """Create a dictionary with snakecase keys derived from custom object type camelcase class names.

        Returns:
            dict[str, Type]: Dictionary with snakecase strings of all subclasses of PythonObjectJson as keys and
            subclasses as values.

        """
        # retrieve all class subclasses after base class
        return {derive_custom_object_key(cls): cls for cls in self.__class__.__mro__[-2].__subclasses__()}

    def serialize(self) -> Dict[str, Any]:
        """Create a serializable dictionary from the class instance.

        Returns:
            dict[str, Any]: Serializable dictionary representing the class instance.

        """
        return serialize(self, list(self._base_subclasses().values()))

    def to_json_str(self) -> str:
        """Serialize the class instance to a JSON string.

        Returns:
            str: JSON string derived from the serializable version of the class instance.

        """
        return json.dumps(self.serialize(), ensure_ascii=False, indent=2)

    def from_json_str(self, json_str: str) -> None:
        """Load the class instance from a JSON string.

        Args:
            json_str (str): JSON string to be deserialized into the class instance.

        Returns:
            None

        """
        loaded_class_instance = deserialize(json.loads(json_str), self._base_subclasses())

        # update the class instance attributes with the attributes from the loaded class instance
        vars(self).update(**vars(loaded_class_instance))

    def save_to_json_file(self, json_file_path: Path) -> None:
        """Save the class instance to a JSON file.

        Args:
            json_file_path (Path): Target JSON file path to which the class instance will be saved.

        Returns:
            None

        """
        if not json_file_path.exists():
            json_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(json_file_path, "w", encoding="utf-8") as json_file_out:
            # TODO: fix incorrect file input type warning for json.dump from PyCharm bug https://youtrack.jetbrains.com/issue/PY-73050/openfile.txt-r-return-type-should-be-inferred-as-TextIOWrapper-instead-of-TextIO
            # noinspection PyTypeChecker
            json.dump(self.serialize(), json_file_out, ensure_ascii=False, indent=2)

    def load_from_json_file(self, json_file_path: Path) -> None:
        """Load the class instance from a JSON file.

        Args:
            json_file_path (Path): Target JSON file path from which the class instance will be loaded.

        Returns:
            None

        """
        if not json_file_path.exists():
            raise FileNotFoundError(f"File {json_file_path} does not exist. Unable to load saved data.")

        with open(json_file_path, "r", encoding="utf-8") as json_file_in:
            loaded_class_instance = deserialize(json.load(json_file_in), self._base_subclasses())
            vars(self).update(**vars(loaded_class_instance))
