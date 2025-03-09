#!/usr/bin/env python3 
import pytest
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from suppliers.supplier_3schem import Supplier3SChem as Supplier

query = 'cleaner'


class TestClass:
    _results = None
    _results2 = None

    @pytest.fixture
    def valid_results(self):
        if not self._results:
            try:
                self._results = Supplier(query)
            except Exception as e:
                self._results = e
        return self._results  
    
    @pytest.fixture
    def invalid_results(self):
        if not self._results2:
            try:
                self._results2 = Supplier('mumbojumboshouldnotfindaresult')
            except Exception as e:
                self._results2 = e
        return self._results2  

    @pytest.mark.first
    def test_valid_query(self, valid_results):
        assert isinstance(valid_results, Exception) is False

    @pytest.mark.second
    def test_valid_results(self, valid_results):
        assert len(valid_results) > 0

    @pytest.mark.first
    def test_invalid_query(self, invalid_results):
        assert isinstance(invalid_results, Exception) is False

    @pytest.mark.second
    def test_invalid_results(self, invalid_results):
        assert len(invalid_results) == 0