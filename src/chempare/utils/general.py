from __future__ import annotations

import os
import platform
import plistlib
import random
import string
import sys
import math
import time
from collections.abc import Callable
from collections.abc import Iterable
from functools import reduce
from pathlib import Path
from typing import Literal
from typing import NewType
from typing import TYPE_CHECKING
from urllib.parse import parse_qs
from urllib.parse import urlparse
import regex
from str2bool import str2bool

if TYPE_CHECKING:
    from typing import Any, Callable, Iterable, LiteralString
    from datatypes import PrimitiveType  # , Undefined

    # # Undefined = Enum('Undefined', ['undefined'])
    # # undefined = Undefined.undefined
    # Undefined = NewType('Undefined', str)

    # UndefinedStr = str | Undefined
    # undef = Undefined('undefined')

Undefined = NewType('Undefined', str)
undefined = str | Undefined


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
        result = reduce(dict.__getitem__, keys, dict_)
    except (KeyError, TypeError):
        return default
    else:
        return result


def cast(value: str) -> int | float | str | bool | None:
    """
    Cast a str value to its most likely primitive type.

    Args:
        value (str): Value to cast

    Returns:
        PrimitiveType | None: Casted result

    Example:
        >>> from chempare import utils
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
    if str2bool(value) is True:
        return True

    # Boolean type False
    if str2bool(value) is False:
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
    setting: str, default: PrimitiveType | None | Literal[Undefined.undefined] = undefined, typecast: bool = True
) -> PrimitiveType | None:
    """
    The getenv function retrieves an environment variable value, with an optional default value and typecasting support.

    :param setting: The `setting` parameter is a string that represents the name of the environment variable that you want
    to retrieve the value for
    :type setting: str
    :param default: The `default` parameter in the `getenv` function is used to specify a default value that will be
    returned if the environment variable specified by the `setting` parameter is not found in the system environment
    variables. If no `default` value is provided, the function will raise a `ValueError
    :type default: PrimitiveType | None | type[Undefined]
    :param typecast: The `typecast` parameter in the `getenv` function determines whether the retrieved environment variable
    should be typecasted to a string or not. If `typecast` is set to `True`, the function will attempt to cast the retrieved
    value to a string before returning it. If `type, defaults to True
    :type typecast: bool (optional)
    :return: The `getenv` function returns the value of the specified environment variable `setting` if it is found in the
    environment variables. If the `setting` is not found and a `default` value is provided, it returns the `default` value.
    If the `setting` is not found and no `default` value is provided, it raises a `ValueError`.
    """
    if setting not in os.environ and default is undefined:
        raise ValueError(f"Environment variable '{setting}' not set.")

    value = os.getenv(setting, default)

    if typecast is False:
        return value  # type: ignore

    return cast(str(value).strip())


def find_first(arr: Iterable, condition: Callable) -> Any:
    """
    The `find_first` function returns the first element in an iterable that satisfies a given condition.

    :param arr: An iterable object (list, tuple, etc.) containing elements to be checked against the condition function
    :type arr: Iterable
    :param condition: The `condition` parameter is a function that takes an element from the `arr` iterable as input and
    returns a boolean value based on some criteria. This function is used to filter elements from the `arr` iterable, and
    the `find_first` function returns the first element in the iterable that satisfies
    :type condition: Callable
    :return: The `find_first` function returns the first element in the `arr` iterable that satisfies the `condition`
    function. If no element satisfies the condition, it returns `None`.
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


def replace_dict_values_by_value(
    obj: dict, find_value: PrimitiveType | None, replace_value: PrimitiveType
) -> dict[str, str]:
    """
    The function `replace_dict_values_by_value` recursively replaces specified values in a
    dictionary with a new value.

    :param obj: A dictionary object that you want to modify by replacing certain values
    :type obj: dict
    :param find_value: The `find_value` parameter in the `replace_dict_values_by_value` function
    is the value that you want to search for in the dictionary `obj`. If a key in the dictionary
    has this `find_value`, it will be replaced with the `replace_value` provided in the args
    :type find_value: PrimitiveType | None
    :param replace_value: The `replace_value` parameter in the `replace_dict_values_by_value`
    function is the value that will replace any matching values found in the dictionary. For
    example, if you want to replace all occurrences of a specific value with a new value in the
    dictionary, you would pass the new value as the `replace_value`
    :type replace_value: PrimitiveType
    :return: The function `replace_dict_values_by_value` returns a dictionary where the values
    have been replaced based on the provided criteria.
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


def split_set_cookie(set_cookie: str) -> list:
    """
    split_set_cookie Splits a 'set-cookie' header up into its segments.

    This is needed because you typically split them up by the ',' (comma), but then sometimes
    there's a date included in there, which is in the format of "Sun, 20 Apr 2025 15:51:54 GMT",
    which causes issues with splitting by commas.

    :param set_cookie: The set-cookie value from the header
    :type set_cookie: str
    :return: list of set-cookie values, split by the comma delimiter
    :rtype: list
    """
    return regex.split(r'(?<!Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s?', set_cookie)


def parse_cookie(value: str) -> dict[str, Any] | None:
    """
    Get cookie name/value out of the full set-cookie header segment.

    Args:
        value (str): The set-cookie segment.

    See:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie

    Returns:
        dict[str, str]: The cookie info (name, value, attrs, etc)

    Example:
        >>> utils.parse_cookie("ssr-caching=cache#desc=hit#varnish=hit_hit#dc#desc=fastly_g; max-age=20")
        {'name': 'ssr-caching', 'value': 'cache#desc=hit#varnish=hit_hit#dc#desc=fastly_g', 'max-age': '20'}
        >>> utils.parse_cookie("client-session-bind=7435e070-c09e-4b97-9b70-b679273af80a; Path=/; Secure; SameSite=Lax;")
        {'name': 'client-session-bind', 'value': '7435e070-c09e-4b97-9b70-b679273af80a', 'path': '/', 'secure': True, 'samesite': 'Lax'
        >>> utils.parse_cookie("server-session-bind=7435e070-c09e-4b97-9b70-b679273af80a; Path=/; Secure; SameSite=Lax; HttpOnly;")
        {'name': 'server-session-bind', 'value': '7435e070-c09e-4b97-9b70-b679273af80a', 'path': '/', 'secure': True, 'samesite': 'Lax', 'httponly': True}
    """

    cookie_matches = regex.match(
        r'^(?P<name>[a-zA-Z0-9_-]+)=(?P<value>[^;]+)(?:$|;\s)(?P<args>(.*)+)?$', value, regex.IGNORECASE
    )

    # print(cookie_matches.capturesdict())

    cookie_match_dict = cookie_matches.capturesdict()

    result = {"name": cookie_match_dict.get('name', [None])[0], "value": cookie_match_dict.get('value', [None])[0]}

    args = cookie_match_dict.get('args', [])[0].rstrip(';').split(';')

    cookie_args = {}

    for a in args:
        arg_segs = a.strip().split('=')
        if len(arg_segs) == 1:
            cookie_args[arg_segs[0].lower()] = True
            continue

        cookie_args[arg_segs[0].lower()] = arg_segs[1]

    result.update(cookie_args)

    return result


def random_string(max_length: int = 10, include_special: bool = False) -> str:
    """
    Generate random string

    Args:
        max_length (int, optional): Length to generate string to. Defaults to 10
        include_special (bool, optional): Include special chars in output.
                                          Defaults to False

    Returns:
        str: Random string, {len} chars long
    """
    if isinstance(max_length, int) is False:
        max_length = 10

    # ascii_letters = abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    # digits = 0123456789
    # punctuation = !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
    char_list: LiteralString = string.ascii_letters + string.digits

    if include_special is True:
        char_list += string.punctuation

    # trunk-ignore(bandit/B311)
    return str("".join(random.choice(char_list) for _ in range(max_length)))


def set_multiple_defaults(dictionary, defaults):
    for key, value in defaults.items():
        dictionary.setdefault(key, value)


def split_array_into_groups(arr: list, size: int = 2) -> list:
    """
    Splits an array into sub-arrays of 2 elements each.

    Args:
        arr: The input array.
        size: Size to group array elements by

    Returns:
        A list of sub-arrays, where each sub-array contains {size} elements,
        or an empty list if the input array is empty.

    Example:
        >>> utils.split_array_into_groups([
        ...    'Variant', '500 g', 'CAS', '1762-95-4'
        ... ])
        [['Variant', '500 g'],['CAS', '1762-95-4']]
    """

    result = []
    for i in range(0, len(arr), size):
        result.append(arr[i : i + size])

    return result


def nested_arr_to_dict(arr: list[list]) -> dict | None:
    """
    Takes an array of arrays (ie: result from
    utils.split_array_into_groups) and converts that into a dictionary.

    Args:
        arr (list[list]): The input array.

    Returns:
        Optional[dict]: A dictionary based off of the input alues

    Example:
        >>> utils.nested_arr_to_dict([["foo","bar"], ["baz","quux"]])
        {'foo':'bar','baz":'quux"}
    """

    # Only works if the array has even amount of elements
    if len(arr) % 2 != 0:
        return None

    grouped_elem = split_array_into_groups(arr, 2)
    variant_dict = [dict(item) for item in grouped_elem]

    return variant_dict[0] or None


def get_param_from_url(url: str, param: str | None = None) -> Any | None:
    """
    Get a specific arameter from a GET URL

    Args:
        url (str): HREF address
        param (str): Param key to find (optional)

    Returns:
        Any: Whatver the value was of the key, or nothing

    Example:
        >>> utils.get_param_from_url(
        ...    'http://google.com?foo=bar&product_id=12345'
        ... )
        {'foo':'bar','product_id':'12345'}
        >>> utils.get_param_from_url(
        ...    'http://google.com?foo=bar&product_id=12345', 'product_id'
        ... )
        '12345'
    """

    parsed_url = urlparse(url)
    parsed_query = parse_qs(parsed_url.query)

    # Replace any ['values'] with just 'values'
    parsed_query = {k: v[0] if len(v) == 1 else v for k, v in parsed_query.items()}

    if not param:
        return parsed_query

    # If no specific parameter was defined, then just return this
    if param not in parsed_query:
        return None

    if not parsed_query[param]:
        return None

    return parsed_query[param]


def epoch() -> int:
    """
    Get epoch string - Used for unique values in searches (sometimes _)

    Returns:
        int: Current time in epoch
    """

    return math.floor(time.time() * 1000)
