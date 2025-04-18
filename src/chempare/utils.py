import hashlib
import json
import os
import platform
import plistlib
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from chempare.datatypes import TypeLowLevel


def get_env(setting: str, default: TypeLowLevel | None = None) -> TypeLowLevel | None:
    value = os.getenv(setting, default)
    # If it's not a string, then its probably a valid type..
    if isinstance(value, str) is False:
        return value

    # Most castable values just need to be trimmed to be compatible
    value = str(value).strip()

    if not value or value.isspace():
        return None

    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    try:
        return int(value)
    except Exception:
        pass

    try:
        return float(value)
    except Exception:
        pass

    return value


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

            data = find_first(data["LSHandlers"], lambda h: h.get("LSHandlerURLScheme") in ['http', 'https'])

            if not isinstance(data, dict):
                return None

            return data.get('LSHandlerRoleAll').split('.')[1]
        except:
            pass

    if platform.system() == 'Darwin':
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


NonIterable = str | int | float | bool | None


def replace_dict_values_by_value(obj: dict, find_value: NonIterable, replace_value: NonIterable) -> dict[str, str]:
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
