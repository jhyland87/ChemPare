from __future__ import annotations
from typing import Mapping, overload
from bs4.element import NavigableString, Tag, PageElement
import re


@overload
def text_from_element(element: None) -> None: ...


@overload
def text_from_element(element: PageElement) -> str: ...


@overload
def text_from_element(element: Tag | NavigableString) -> str: ...


def text_from_element(element) -> str | None:
    if isinstance(element, Tag):
        return str(element.decode_contents())

    if isinstance(element, NavigableString):
        return str(element.strings)

    if isinstance(element, NavigableString):
        return element.get_text(strip=True)


def parse_css_selector(selector: str) -> list[Mapping]:
    """
    parse_css_selector - Parse a CSS selector

    Parses a selector to get a list of groupdicts, each of which could contain the
    element type (div, span, etc), ID, class, and [prop=val] attributes

    :param selector: CSS Selector path
    :type selector: str
    :return: List of selector dictionaries
    :Example:
    >>> import chempare.utils as utils
    >>> utils.parse_css_selector('div#foo')
    [{'elem': 'div', 'id': 'foo', 'class': None, 'attr_name': None, 'attr_val': None}]
    >>> utils.parse_css_selector('div#foo > span.bar')
    [
      {'elem': 'div', 'id': 'foo', 'class': None, 'attr_name': None, 'attr_val': None},
      {'elem': 'span', 'id': None, 'class': 'bar', 'attr_name': None, 'attr_val': None}
    ]
    >>> utils.parse_css_selector('div#foo > span.bar > div.foo[idk=wtf]')
    [
      {'elem': 'div', 'id': 'foo', 'class': None, 'attr_name': None, 'attr_val': None},
      {'elem': 'span', 'id': None, 'class': 'bar', 'attr_name': None, 'attr_val': None},
      {'elem': 'div', 'id': None, 'class': 'foo', 'attr_name': 'idk', 'attr_val': 'wtf'}
    ]
    """
    selectors: list[str] = selector.split('>')

    results: list[Mapping] = []
    for sel in selectors:
        sel = sel.strip()
        matches = re.match(
            r"^(?P<elem>[a-zA-Z\._-]+?)(?:#(?P<id>[a-zA-Z\._-]+?))?(?:\.(?P<class>(?:[a-zA-Z\._-]+))?)?(?:\[(?P<attr_name>[a-zA-Z\._-]+)=(?P<attr_val>.+)\])?$",
            sel,
        )

        if matches is None:
            continue
        results.append(matches.groupdict())

    return results
