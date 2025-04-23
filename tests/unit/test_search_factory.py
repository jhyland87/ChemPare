from __future__ import annotations

from chempare.search_factory import SearchFactory


# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

# from search_factory import SearchFactory


def test_chemical_name_query():
    res = None
    exception = None
    res = SearchFactory("water")

    assert isinstance(exception, Exception) is False
    assert len(res) > 0


# def test_chemical_cas_query():
#     res = None
#     exception = None
#     try:
#         res = SearchFactory('7732-18-5')
#     except Exception as e:
#         exception = e

#     assert isinstance(exception, Exception) is False
#     assert len(res) > 0
