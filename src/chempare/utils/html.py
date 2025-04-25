from __future__ import annotations

import re
from collections.abc import Mapping
from typing import overload

from bs4 import BeautifulSoup
from bs4.element import NavigableString
from bs4.element import PageElement
from bs4.element import Tag


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


def bs4_css_selector(
    element: BeautifulSoup, selector: str
) -> PageElement | None:  # -> None | BeautifulSoup | Tag | NavigableString | Any:
    selectors = parse_css_selector(selector)
    cursor: PageElement | None = element
    for sel in selectors:
        print("Iterating over", sel)
        find_args = {"attrs": {}, "name": sel["elem"]}

        if (class_ := sel.get("class", None)) is not None:
            find_args["class_"] = class_

        if (elem_id := sel.get("id", None)) is not None:
            find_args["id"] = elem_id

        if (place := cursor.find(**find_args)) is not None:
            cursor = place
        else:
            cursor = None
            break

    return cursor


# product_page_soup.find("div", class_="woocommerce-product-details__short-description")
#             .find('table')
#             .find('tbody')
#             .find_all('tr')


def parse_css_selector(selector: str) -> list[Mapping]:
    """
    parse_css_selector - Parse a CSS selector

    Parses a selector to get a list of groupdicts, each of which could contain the
    element type (div, span, etc), ID, class, and [prop=val] attributes

    https://regex101.com/r/oCq8X8/1

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
