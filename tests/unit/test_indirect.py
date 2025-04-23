# content of ./test_parametrize.py
import pytest


def pytest_generate_tests(metafunc):
    # called once per each test function
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = sorted(funcarglist[0])
    metafunc.parametrize(argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist])


class BaseTest:
    # a map specifying multiple argument sets for a test method
    params = {"test_good_queries": [], "test_bad_queries": []}

    @classmethod
    def setup_class(cls):
        print("In setup..")

    @classmethod
    def teardown_class(cls):
        print("In teardown..")

    def test_good_queries(self, query):
        assert query != "foobarbaz"

    def test_bad_queries(self, query):
        assert query == "foobarbaz"


class TestClassA(BaseTest):
    # a map specifying multiple argument sets for a test method
    params = {
        "test_good_queries": [dict(query="acid"), dict(query="123123-12-5")],
        "test_bad_queries": [dict(query="foobarbaz")],
    }


class TestClassB(BaseTest):
    # a map specifying multiple argument sets for a test method
    params = {
        "test_good_queries": [dict(query="water"), dict(query="9994-12-5")],
        "test_bad_queries": [dict(query="idkwtf"), {"query": "99999-99-9"}],
    }
