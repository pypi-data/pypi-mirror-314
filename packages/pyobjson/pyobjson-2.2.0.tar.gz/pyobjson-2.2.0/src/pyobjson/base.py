"""Python Object JSON Tool pyobjson.base module.

Attributes:
    __author__ (str): Python package template author.
    __email__ (str): Python package template author email.

"""
__author__ = "Wren J. Rudolph for Wrencode, LLC"
__email__ = "dev@wrencode.com"

import json
from pathlib import Path
from typing import Dict, Type, Any

from pyobjson.data import serialize, deserialize
from pyobjson.utils import derive_custom_class_key


class PythonObjectJson(object):
    """Base Python Object with JSON serialization and deserialization compatibility.
    """

    def __init__(self, **kwargs):
        """Instantiate the PythonObjectJson class with all keyword arguments.

        Args:
            kwargs (dict): Key/value pairs to be passed to the PythonObjectJson class.

        """
        vars(self).update(kwargs)

    def __str__(self):
        return self.to_json_str()

    def __repr__(self):
        return self.serialize()

    # @staticmethod
    # def _complex_json_handler(obj: Any) -> Any:
    #     """Custom handler to allow custom objects to be serialized into JSON.
    #
    #     Args:
    #         obj (Any): Custom object to be serialized into JSON.
    #
    #     Returns:
    #         obj (Any): Serializable version of the custom object.
    #
    #     """
    #     if hasattr(obj, "serialize"):
    #         return obj.serialize()
    #     else:
    #         try:
    #             return str(obj)
    #         except TypeError:
    #             raise TypeError(f"Object of type {type(obj)} with value of {repr(obj)} is not JSON serializable.")

    def _base_subclasses(self) -> Dict[str, Type]:
        """Create dict with snakecase keys derived from custom object type camelcase class names.

        Returns:
            dict[str, Type]: Dictionary with snakecase strings of all subclasses of PythonObjectJson as keys and
            subclasses as values.

        """
        # retrieve all class subclasses after base class
        return {derive_custom_class_key(cls): cls for cls in self.__class__.__mro__[-2].__subclasses__()}

    def serialize(self) -> Dict[str, Any]:
        """Class method to serialize the class instance into a serializable dictionary.

        Returns:
            dict[str, Any]: Serializable dictionary.

        """
        return serialize(self, list(self._base_subclasses().values()))

    def to_json_str(self) -> str:
        """Serialize the class object to a JSON string.

        Returns:
            str: JSON string derived from the serializable version of the class object.

        """
        return json.dumps(
            self.serialize(),
            ensure_ascii=False,
            indent=2,
            # default=self._complex_json_handler,
        )

    def from_json_str(self, json_str: str) -> None:
        """Load the class object from a JSON string.

        Args:
            json_str (str): JSON string to be deserialized into the class object.

        Returns:
            None

        """
        loaded_class_instance = deserialize(json.loads(json_str), self._base_subclasses())

        # update the class instance attributes with the attributes from the loaded class instance
        vars(self).update(**vars(loaded_class_instance))

    def save_to_json_file(self, json_file_path: Path) -> None:
        """Save the class object to a JSON file.

        Args:
            json_file_path (Path): Target JSON file path to which the class object will be saved.

        Returns:
            None

        """
        if not json_file_path.exists():
            json_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(json_file_path, "w", encoding="utf-8") as json_file_out:
            # TODO: fix incorrect file input type warning for json.dump from PyCharm bug https://youtrack.jetbrains.com/issue/PY-73050/openfile.txt-r-return-type-should-be-inferred-as-TextIOWrapper-instead-of-TextIO
            # noinspection PyTypeChecker
            json.dump(
                serialize(self, list(self._base_subclasses().values())),
                json_file_out,
                ensure_ascii=False,
                indent=2,
                # default=self._complex_json_handler
            )

    def load_from_json_file(self, json_file_path: Path) -> None:
        """Load the class object from a JSON file.

        Args:
            json_file_path (Path): Target JSON file path from which the class object will be loaded.

        Returns:
            None

        """
        if not json_file_path.exists():
            raise FileNotFoundError(
                f"File {json_file_path} does not exist. Unable to load saved data."
            )

        with open(json_file_path, "r", encoding="utf-8") as json_file_in:
            loaded_class_instance = deserialize(json.load(json_file_in), self._base_subclasses())
            vars(self).update(**vars(loaded_class_instance))
