"""
Utility class meant to provide functionality to any inheriting classes"""
from __future__ import annotations

import re
from typing import Any


def find_cas(value: str) -> str | None:
    """
    Parse a string for CAS values, return the first valid one

    Args:
        value (str): String content with possible CAS issues

    Returns:
        Optional[str]: First valid CAS number, or nothing
    """

    matches = re.findall(r"([0-9]{2,7}-[0-9]{2}-[0-9])", value)

    for m in matches:
        if not is_cas(m):
            continue

        return m
    return None


def is_cas(value: Any) -> bool:
    """
    Check if a string is a valid CAS registry number

    CAS numbers are always in a format of three segments of numerical values:
        1234-56-6

    The first segment can be from 2 to 7 intigers (needs to be at least one non-zero value),
    and the second is always 2 integers. These are basically just unique numbers, but there's no
    established numbering system or other restrictions.
    The third segment is one integer, and that is the checksum of the first two segments.

    https://regex101.com/r/xPF1Yp/2
    (?P<seg_a>[0-9]{2,7})-(?P<seg_b>[0-9]{2})-(?P<checksum>[0-9])

    The checksum is calculated by taking the first two segments and iterating over each
    individual intiger in reverse order, multiplying each by its position, then taking
    the modulous of the sum of those values.

    For example, 1234-56-6 is valid because the result of the below equation matches the checksum, (which is 6)
        (6*1 + 5*2 + 4*3 + 3*4 + 2*5 + 1*6) % 10 == 6

    This can be simplified in the below aggregation:
        cas_chars = [1, 2, 3, 4, 5, 6]
        sum([(idx+1)*int(n) for idx, n
            in enumerate(cas_chars[::-1])]) % 10

    See:
        https://www.cas.org/training/documentation/chemical-substances/checkdig
        https://www.allcheminfo.com/chemistry/cas-number-lookup.html

    Args:
        value (str): The value to determine if its a CAS # or not

    Returns:
        bool: True if its a valid format and the checksum matches

    Example:
        >>> utils.is_cas("1234-56-6")
        True
        >>> utils.is_cas("50-00-0")
        True
        >>> utils.is_cas("1234-56-999")
        False
        >>> utils.is_cas("1234-56")
        False
        >>> utils.is_cas("1234-56-0")
        False
        >>> utils.is_cas("0000-00-0")
        False
        >>> utils.is_cas("00-10-0")
        False
    """

    if isinstance(value, str) is False:
        return False

    # value='1234-56-6'
    # https://regex101.com/r/xPF1Yp/2
    cas_pattern_check = re.match(r"^(?P<seg_a>[0-9]{2,7})-(?P<seg_b>[0-9]{2})-(?P<checksum>[0-9])$", value)

    if cas_pattern_check is None:
        return False

    cas_dict = cas_pattern_check.groupdict()
    # cas_dict = dict(seg_a="1234", seg_b="56", checksum="6")

    if int(cas_dict["seg_a"]) == 0:
        return False

    cas_chars = list(cas_dict["seg_a"] + cas_dict["seg_b"])
    # cas_chars = ["1","2","3","4","5","6"]

    checksum = sum([(idx + 1) * int(n) for idx, n in enumerate(cas_chars[::-1])]) % 10
    # checksum = 6

    return int(checksum) == int(cas_dict["checksum"])
