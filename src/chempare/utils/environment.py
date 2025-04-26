from __future__ import annotations

import math
import os
import platform
import plistlib
import time
from pathlib import Path
from typing import TYPE_CHECKING

import chempare.utils as utils
from chempare.exceptions import UnsupportedPlatformError

if TYPE_CHECKING:
    from datatypes import PrimitiveType  # , Undefined
    from typing import Any
    # # Undefined = Enum('Undefined', ['undefined'])
    # # undefined = Undefined.undefined
    # Undefined = NewType('Undefined', str)

    # UndefinedStr = str | Undefined
    # undef = Undefined('undefined')

# Undefined = NewType('Undefined', str)
# undefined = str | Undefined

from datatypes import Undefined, undefined


def epoch() -> int:
    """
    Get epoch string - Used for unique values in searches (sometimes _)

    Returns:
        int: Current time in epoch
    """

    return math.floor(time.time() * 1000)


def get_default_browser() -> str | None:
    """
    Get the default browser for the current system. This is used for if were given permission
    to use the browsers cookies.

    Returns:
        str: Browser
    """

    # all_browsers = [chrome, chromium, opera, opera_gx, brave, edge, vivaldi, firefox, librewolf,
    # safari, lynx, w3m, arc]
    def _for_darwin() -> str | None:
        """
        Check the with the com.apple.LaunchServices to see what the default 'LSHandler' for the schemes
        http or https are. It should be someting like com.brave.browser, which this would then return
        'brave'

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

            data = utils.find_first(
                data["LSHandlers"], lambda h: h.get("LSHandlerURLScheme") in ["http", "https"]
            )

            if not isinstance(data, dict):
                return None

            return data.get("LSHandlerRoleAll", "").split(".")[1]
        except Exception as e:
            print(e)
            pass
        return None

    if platform.system() == "Darwin":
        return _for_darwin()

    raise UnsupportedPlatformError(
        f"ERROR: No logic on getting the default browser for your platform: {platform.system()}\n"
    )


def getenv(
    setting: str, default: PrimitiveType | Undefined | None = undefined, typecast: bool = True
) -> PrimitiveType | None:
    """
    The getenv function retrieves an environment variable value, with an optional default value and
    typecasting support.
    :param setting: The `setting` parameter is a string that represents the name of the environment
    variable that you want
    to retrieve the value for
    :type setting: str
    :param default: The `default` parameter in the `getenv` function is used to specify a default
    value that will be
    returned if the environment variable specified by the `setting` parameter is not found in the
    system environment variables. If no `default` value is provided, the function will raise a
    `ValueError` exception
    :type default: PrimitiveType | None | type[Undefined]
    :param typecast: The `typecast` parameter in the `getenv` function determines whether the
    retrieved environment variable should be typecasted to a string or not. If `typecast` is set to
    `True`, the function will attempt to cast the retrieved value to a string before returning it.
    :type typecast: bool (optional)
    :return: The `getenv` function returns the value of the specified environment variable `setting`
    if it is found in the environment variables. If the `setting` is not found and a `default` value
    is provided, it returns the `default` value. If the `setting` is not found and no `default`
    value is provided, it raises a `ValueError`.
    """
    if setting not in os.environ and default is undefined:
        raise ValueError(f"Environment variable '{setting}' not set.")

    value: Any | None = os.getenv(setting, default)

    if typecast is False:
        return value  # type: ignore

    return utils.cast(str(value).strip())
