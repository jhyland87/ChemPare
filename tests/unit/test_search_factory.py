"""Biofuran Chem supplier test module"""
from __future__ import annotations

from collections.abc import Iterable

import chempare.suppliers
import pytest
import requests
from chempare.exceptions import NoProductsFoundError
from chempare.search_factory import SearchFactory
from pytest import MonkeyPatch

from tests import mock_request_cache

# from datatypes import ProductType


monkeypatch = MonkeyPatch()
