from __future__ import annotations

import functools
import math
import time
from collections import OrderedDict
from ctypes import util
from decimal import Decimal
from typing import Literal
from unittest.mock import patch

import chempare.utils as utils
import pytest
from bs4 import BeautifulSoup
from datatypes import PriceType
from datatypes import QuantityType
from datatypes import Undefined
from datatypes import undefined
from datatypes import UndefinedType
from price_parser.parser import Price


def sort_and_compare(dict1: dict, dict2: dict) -> bool | Exception:
    try:
        return dict(OrderedDict(sorted(dict1.items()))) == dict(OrderedDict(sorted(dict2.items())))
    except Exception as e:
        return e


@pytest.mark.parametrize(
    ("html", "selector", "expected_result"),
    [
        ("<div>Hello</div>", "div", "Hello"),
        ("<span><div>Hello</div></span>", "span > div", "Hello"),
        ("<span>Foo</span><span id=\"foo\"><div>Hello</div></span>", "span#foo > div", "Hello"),
        (
            "<span>Foo</span><span id=\"foo\"><div class=\"baz\">Hello</div><div class=\"bar\">Hello</div></span>",
            "span#foo > div.baz",
            "Hello",
        ),
        ("<foo>nada</foo>", "badpath", None),
    ],
    ids=["div", "span > div", "span#foo > div", "span#foo > div.baz", "badpath"],
)
def test_bs4_css_selector(html, selector, expected_result):
    soup = BeautifulSoup(html, "html.parser")
    result = utils.bs4_css_selector(soup, selector)

    if expected_result is None:
        assert expected_result == None
    else:
        assert result.getText() == expected_result


@pytest.mark.parametrize(
    ("selector", "expected_result"),
    [
        ("div.class", [{'elem': 'div', 'id': None, 'class': 'class', 'attr_name': None, 'attr_val': None}]),
        ("div#id", [{'elem': 'div', 'id': 'id', 'class': None, 'attr_name': None, 'attr_val': None}]),
        ("div#id.class", [{'elem': 'div', 'id': 'id', 'class': 'class', 'attr_name': None, 'attr_val': None}]),
        (
            "div#id.class[attr=name]",
            [{'elem': 'div', 'id': 'id', 'class': 'class', 'attr_name': 'attr', 'attr_val': 'name'}],
        ),
        (
            "div#id.class[attr=name] > div#id.class[attr=name]",
            [
                {'elem': 'div', 'id': 'id', 'class': 'class', 'attr_name': 'attr', 'attr_val': 'name'},
                {'elem': 'div', 'id': 'id', 'class': 'class', 'attr_name': 'attr', 'attr_val': 'name'},
            ],
        ),
        ("$$%$", []),
    ],
    ids=[
        "div.class",
        "div#id",
        "div#id.class",
        "div#id.class[attr=name]",
        "div#id.class[attr=name] > div#id.class[attr=name]",
        "Bad selector",
    ],
)
def test_parse_css_selector(selector, expected_result):
    path = utils.parse_css_selector(selector)

    assert type(path) is type(expected_result), "Result does not match expected type"

    assert len(path) == len(expected_result), "Submatch count incorrect"

    assert isinstance(path, list), "Result is not a list"

    assert str(path) == str(expected_result), "Comparison failed"
