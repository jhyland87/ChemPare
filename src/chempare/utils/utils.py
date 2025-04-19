import hashlib
import json
import os
import platform
import plistlib
import sys
from collections.abc import Iterable
from functools import reduce
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Iterable

from chempare.datatypes import PrimitiveType
from chempare.datatypes import Undefined


def get_nested(dict_: dict, *keys, default: Any = None) -> Any:
    """
    Get a nested value from a dictionary

    Args:
        dict_ (dict): Dictionary to iterate over
        keys (list[str]): Keys to drill down with
        default (Any, optional): Default value. Defaults to None.

    Returns:
        Any: Result, if somethig was found

    Example:
        >>> d = {"foo":{"bar":{"baz":"test"}}}
        >>> get_nested(d, "foo","bar","baz")
        test
        >>> get_nested(d, "foo","bar","bazzzz")
        None
        >>> get_nested(d, "foo","bar","bazzzz", default="no bazzzz")
        no bazzzz
        >>> get_nested(d, "foo","bar")
        {'baz': 'test'}
    """

    try:
        X = reduce(dict.__getitem__, keys, dict_)
    except (KeyError, TypeError):
        return default
    else:
        return X


# PYTEST_CURRENT_TEST
# DEBUGPY_RUNNING


def cast(value: str) -> PrimitiveType | None:
    """
    Cast a str value to its most likely primitive type.

    Args:
        value (str): Value to cast

    Returns:
        PrimitiveType | None: Casted result

    Example:
        >>> from chempare.utils import utils
        >>> utils.cast("123")
        123
        >>> utils.cast("123.34")
        123.34
        >>> utils.cast("123.34000")
        123.34
        >>> utils.cast("true")
        True
        >>> utils.cast("FALSE")
        False
        >>> utils.cast("None")
        >>> utils.cast("null")
        >>> utils.cast("0")
        0
        >>> utils.cast("Test")
        'Test'
        >>> utils.cast(True)
        ValueError: Unable to cast value type <class 'bool'> - Must be a string
    """

    # If it's not a string, then its probably a valid type..
    if isinstance(value, str) is False:
        raise ValueError(f"Unable to cast value type '{type(value).__name__}' - Must be a string")

    # Most castable values just need to be trimmed to be compatible
    value = value.strip()

    # Account for any Null-ish types (None, null, "", etc)
    if not value or value.lower() == "none" or value.lower() == "null" or value.isspace():
        return None

    # Boolean type True
    if value.lower() == "true":
        return True

    # Boolean type False
    if value.lower() == "false":
        return False

    try:
        return int(value)
    except (ValueError, TypeError):
        pass

    try:
        return float(value)
    except (ValueError, TypeError):
        pass

    return value


def getenv(
    setting: str, default: PrimitiveType | None | type[Undefined] = Undefined, typecast: bool = True
) -> PrimitiveType | None:
    """
    Get an environmental variable. Also casts the value to the most likely type

    Args:
        setting (str): Name of the environmental variable
        default (PrimitiveType | None, optional): Default value of variable.
        cast (bool): Cast the variable to its most likely type. Defaults to True

    Raises:
        ValueError: ValueError if the env var is not set and no default is provided

    Returns:
        PrimitiveType | None: Environmental variable of types: int, float, str,  bool or None

    Example:
        >>> os.environ["FOO"] = "BAR"
        >>> utils.getenv("FOO")
        'BAR'
        >>> utils.getenv("BAZ")
        ValueError: Environment variable 'BAZ' not set.
        >>> utils.getenv("BAZ", None)
        >>> utils.getenv("BAZ", "qux")
        'qux'
        >>> utils.getenv("BAZ", 123)
        123
        >>> utils.getenv("BAZ", "123")
        123
        >>> utils.getenv("DEBUG_LVLd", "123", cast=False)
        '123'
        >>> utils.getenv("BAZ", "test123")
        'test123'
    """
    if setting not in os.environ and default is Undefined:
        raise ValueError(f"Environment variable '{setting}' not set.")

    value = os.getenv(setting, default)

    if typecast is False:
        return value  # type: ignore

    return cast(str(value).strip())


def find_first(arr: Iterable, condition: Callable) -> Any:
    """
    Find the first element in an array that matches a condition

    Args:
        arr (Iterable): Array to iterate over and search
        condition (Callable): Function to do the filtering

    Returns:
        Any: Result from the array
    """

    return next((element for element in arr if condition(element)), None)


def get_default_browser() -> str | None:
    """
    Get the default browser for the current system. This is used for if were given permission
    to use the browsers cookies.

    Returns:
        str: Browser
    """

    # all_browsers = [chrome, chromium, opera, opera_gx, brave, edge, vivaldi, firefox, librewolf, safari, lynx, w3m, arc]
    def _for_darwin() -> str | None:
        """
        Check the with the com.apple.LaunchServices to see what the default 'LSHandler'
        for the schemes http or https are. It should be someting like com.brave.browser,
        which this would then return 'brave'

        Returns:
            str | None: Browser type, if the setting is found.
        """
        try:
            system_preferences = (
                Path.home()
                / "Library"
                / "Preferences"
                / "com.apple.LaunchServices/com.apple.launchservices.secure.plist"
            )

            with system_preferences.open("rb") as fp:
                data = plistlib.load(fp)

            data = find_first(data["LSHandlers"], lambda h: h.get("LSHandlerURLScheme") in ["http", "https"])

            if not isinstance(data, dict):
                return None

            return data.get("LSHandlerRoleAll").split(".")[1]
        except:
            pass

    if platform.system() == "Darwin":
        return _for_darwin()

    sys.stderr.write(f"ERROR: No logic on getting the default browser for your platform: {platform.system()}\n")
    os._exit(1)


def dict_hash(dictionary: dict[str, Any], sort: bool = True) -> str:
    """
    MD5 hash of a dictionary.

    Args:
        dictionary (dict[str, Any]): Dictionary to hash
        sort (bool): Should we sort the dictionary before the checksum?

    Returns:
        str: md5 checksum
    """
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    if sort:
        dictionary = dict(sorted(dictionary.items()))

    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()


def replace_dict_values_by_value(
    obj: dict, find_value: PrimitiveType | None, replace_value: PrimitiveType
) -> dict[str, str]:
    """
    Replace values in a dictionary with another value.

    Args:
        obj (dict): Object to manipulate
        find_value (NonIterable): Value to find
        replace_value (NonIterable): Value to replace it with

    Returns:
        dict[str, str]: Modified object

    Example:
        >>> replace_dict_values_by_value({'foo':'bar','enabled':True,'verbose':False}, True, 'true')
        {'foo':'bar','enabled':'true','verbose':False}
        >>> replace_dict_values_by_value({'foo':'bar','enabled':True,'verbose':False}, 'bar', 'BAR')
        {'foo':'BAR','enabled':True,'verbose':False}
    """
    for k, v in obj.items():
        if isinstance(v, dict):
            obj[k] = replace_dict_values_by_value(v, find_value, replace_value)
        # if key in obj:
        #     obj[key] = replace_value
        if isinstance(find_value, bool):
            if v is find_value:
                obj[k] = replace_value
    return obj
