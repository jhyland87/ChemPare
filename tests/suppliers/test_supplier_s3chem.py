#!/usr/bin/env python3 
import pytest
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from suppliers.supplier_3schem import Supplier3SChem as Supplier

# Base test class
class TestClass:
    _query = 'clean'
    _results = None

    @pytest.fixture
    def results(self):
        if not self._results:
            try:
                self._results = Supplier(self._query)
            except Exception as e:
                self._results = e
        
        return self._results  

# Test cases for a valid search for this supplier
class TestValidSearch(TestClass):
    @pytest.mark.first
    def test_valid_query(self, results):
        assert isinstance(results, Exception) is False
    
    @pytest.mark.second
    def test_valid_results(self, results):
        assert len(results) > 0

# Test cases for invalid searches for this supplier
class TestInvalidSearch(TestClass):
    _query = 'This_should_return_no_results'

    @pytest.mark.first
    def test_valid_query(self, results):
        assert isinstance(results, Exception) is False
    
    @pytest.mark.second
    def test_valid_results(self, results):
        assert len(results) == 0

# Test cases for a valid CAS search for this supplier
@pytest.mark.skip
class TestValidCASSearch(TestClass):
    _query = '7732-18-5'
    _results = None

    @pytest.mark.first
    def test_query(self, results):
        assert isinstance(results, Exception) is False
    
    @pytest.mark.second
    def test_results(self, results):
        assert len(results) > 0


# Test cases for an invalid CAS search for this supplier
@pytest.mark.skip
class TestInvalidCASSearch(TestClass):
    _query = '7782-77-6' # Nitrous acid, too stable to be sold
    _results = None

    @pytest.mark.first
    def test_query(self, results):
        assert isinstance(results, Exception) is False
    
    @pytest.mark.second
    def test_results(self, results):
        assert len(results) == 0