import inspect

from tests.mock_data.curl_request_mocker import CurlRequestMocker
from tests.mock_data.curl_request_mocker import get_nested_value
from tests.mock_data.curl_request_mocker import query_to_filename


def determine_calling_supplier() -> str | None:
    """Determines what supplier module is calling the mocked curl_cffi"""
    stack = inspect.stack()
    return next(
        (
            s[0].f_locals['self'].__class__.__name__
            for s in stack
            if "self" in s[0].f_locals and s[0].f_locals['self'].__class__.__name__ != "MagicMock"
        ),
        None,
    )


class curl_cffi:
    @staticmethod
    def post(path, *args, **kwargs):
        calling_supplier = determine_calling_supplier()
        print(f"{calling_supplier=}")
        if not path.endswith('/multi_search') or 'json' not in kwargs or "searches" not in kwargs["json"]:
            return None

        query = get_nested_value(kwargs, ["json", "searches", 0, "q"])

        if not query:
            return None

        fname = query_to_filename(query)

        mock_response_file = f"supplier_chemsavers/response_data/POST__multi_search__{fname}.json"

        return CurlRequestMocker(file=mock_response_file)

    @staticmethod
    def get(path, *args, **kwargs):
        pass
