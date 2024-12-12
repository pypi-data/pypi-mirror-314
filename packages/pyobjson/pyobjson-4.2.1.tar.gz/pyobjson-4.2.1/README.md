# pyobjson - Python Object JSON Tool

Utility library for serializing/deserializing custom Python objects to/from JSON.

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/wrencode/pyobjson?color=yellowgreen&label=latest%20release&sort=semver)](https://github.com/wrencode/pyobjson/releases/latest)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/wrencode/pyobjson?color=yellowgreen&label=latest%20version&sort=semver)](https://github.com/wrencode/pyobjson/tags)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/wrencode/pyobjson/python-package.yml?color=brightgreen&label=build)](https://github.com/wrencode/pyobjson/actions/workflows/python-package.yml)

[![PyPI](https://img.shields.io/pypi/v/pyobjson.svg?style=flat)](https://pypi.python.org/pypi/pyobjson)
[![PyPI](https://img.shields.io/pypi/dm/pyobjson.svg?style=flat)](https://pypi.python.org/pypi/pyobjson)
[![PyPI](https://img.shields.io/pypi/pyversions/pyobjson.svg?style=flat)](https://pypi.python.org/pypi/pyobjson)
[![PyPI](https://img.shields.io/pypi/l/pyobjson.svg?style=flat)](https://pypi.python.org/pypi/pyobjson)

---

<sub>***Do you like the Python Object JSON Tool? Star the repository on GitHub and please consider helping support its ongoing development:***</sub>

[<img src="https://raw.githubusercontent.com/wrencode/pyobjson/refs/heads/main/docs/wrencode-donation-venmo-qr-code.jpg" width="300"/>](https://venmo.com/wrencode?txn=pay)

<!-- https://venmo.com/<USER_NAME_1>,<USER_NAME_2>...?txn=<charge|pay>&note=<NOTE>&amount=<AMOUNT> -->

---

<div class="hide-next-element"></div>

**[READ THE DOCS HERE!](https://pyobjson.wrencode.dev)**
<br/>
<sup>Detailed documentation can be found at [https://pyobjson.wrencode.dev](https://pyobjson.wrencode.dev).</sup>

<div class="hide-next-element"></div>

&nbsp;

<div class="hide-next-element"></div>

### Table of Contents

<div class="hide-next-element"></div>

* [About](#about)
    * [Dependencies](#dependencies)
    * [Toolchain](#toolchain)
* [Usage](#usage)
    * [Example](#example)
        * [Output](#output)
    * [Saving and Loading](#saving-and-loading)
        * [JSON Files](#json-files)
        * [MongoDB](#mongodb)
        * [PostgreSQL](#postgresql)

<div class="hide-next-element"></div>

---

<a name="about"></a>
### About

The Python Object JSON Tool is a utility library for serializing/deserializing custom Python objects to/from JSON.

<a name="dependencies"></a>
#### Dependencies

The Python Object JSON Tool does not have any third-party dependencies to run the code. It has several development dependencies, which can be seen in the package `pyproject.toml`.

<a name="toolchain"></a>
#### Toolchain

The below tools and resources are used as part of pyobjson:

* [uv](https://github.com/astral-sh/uv) - package management
* [ruff](https://github.com/astral-sh/ruff) - code linting
* [bandit](https://bandit.readthedocs.io/en/latest/) - code security
* [make](https://www.gnu.org/software/make/manual/make.html) - Makefile build automation
* [MkDocs](https://www.mkdocs.org) - package documentation
* [python-dotenv](https://github.com/theskumar/python-dotenv) - programmatic access to environment variables defined in a `.env` file
* [pytest](https://docs.pytest.org/en/stable/) - code testing framework
* [GitHub Actions](https://docs.github.com/en/actions) - CI/CD
* [act](https://github.com/nektos/act) - GitHub Actions testing

---

<a name="usage"></a>
### Usage

The `pyobjson` package is designed to be used as a base class/parent class/superclass to your own custom Python classes in order to provide built-in, convenient serialization/deserialization functionality. Child classes/subclasses of `pyobjson.base.PythonObjectJson` will automatically have the following methods:

* `pyobjson.base.PythonObjectJson.serialize()`: Create a serializable dictionary from the class instance.
* `pyobjson.base.PythonObjectJson.to_json_str()`: Serialize the class instance to a JSON string.
* `pyobjson.base.PythonObjectJson.from_json_str(json_str)`: Load the class instance from a `pyobjson`-formatted JSON string.
* `pyobjson.base.PythonObjectJson.save_to_json_file(json_file_path)`: Save the class instance to a JSON file.
* `pyobjson.base.PythonObjectJson.load_from_json_file(json_file_path)`: Load the class instance from a `pyobjson`-formatted JSON file.

Please reference the **[documentation at https://pyobjson.wrencode.dev](https://pyobjson.wrencode.dev)** for more detailed usage.

<a name="example"></a>
#### Example

```python
from pyobjson.base import PythonObjectJson

class ChildClass(PythonObjectJson):
    
    def __init__(self):
        super().__init__()
        self.message = "Hello, World!"

class ParentClass(PythonObjectJson):
    def __init__(self):
        super().__init__()
        self.child_classes = [ChildClass()]

parent_class = ParentClass()

print(parent_class.to_json_str())
```

<a name="output"></a>
##### Output

```json
{
  "__main__.parentclass": {
    "collection:list.child_classes": [
      {
        "__main__.childclass": {
          "message": "Hello, World!"
        }
      }
    ]
  }
}
```

The above example shows how `pyobjson` can be used to serialize arbitrary custom Python classes into JSON. Additionally, the above [output](#output) JSON can be used to recreate an equivalent class instance by loading the JSON into a custom Python class instance.

<a name="saving-and-loading"></a>
#### Saving and Loading

The `pyobjson.base.PythonObjectJson` parent class *also* provides built-in methods to save/load arbitrary custom Python classes to/from JSON in several ways.

<a name="json-files"></a>
##### JSON Files

* [JSON](https://www.json.org/json-en.html) files *(using **only** Python built-in libraries)*: Use the `PythonObjectJson.save_to_json_file(json_file_path)` and `PythonObjectJson.load_from_json_file(json_file_path)` methods to save/load your custom Python classes to JSON files.

<a name="mongodb"></a>
##### MongoDB

* [MongoDB](https://www.mongodb.com) *(using [`pymongo`](https://pymongo.readthedocs.io/en/stable/))*: ***COMING SOON!***

<a name="postgresql"></a>
##### PostgreSQL

* [PostgreSQL](https://www.postgresql.org) *(using [`psycopg`](https://www.psycopg.org))*: ***COMING SOON!***
