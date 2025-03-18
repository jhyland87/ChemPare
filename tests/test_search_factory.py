# pylint: disable=too-many-arguments
# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-many-positional-arguments
# pylint: disable=broad-exception-caught

from chempare import SearchFactory


def test_chemical_name_query():
    res = None
    exception = None
    try:
        res = SearchFactory("water")
    except Exception as e:
        exception = e

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
