"""Base supplier test class"""

import pytest


class SupplierBaseTest:
    """Base supplier test class"""

    _query = "clean"
    _results = None

    @pytest.fixture()
    def setup(self):
        print("SupplierBaseTest Setup before test")
        yield
        print("SupplierBaseTest Teardown after test")

    def test_base_method(self, setup):
        assert True


# Base test class
@pytest.mark.supplier
class TestClass:
    _query = "clean"
    _results = None

    @pytest.fixture
    def results(self):
        if not self._results:
            try:
                self._results = Supplier(self._query)
            except Exception as e:
                self._results = e

        return self._results
