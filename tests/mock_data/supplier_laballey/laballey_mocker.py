
from tests.mock_data.curl_request_mocker import query_to_filename
from tests.mock_data.curl_request_mocker import get_nested_value
from tests.mock_data.curl_request_mocker import CurlRequestMocker


class curl_cffi:
    @staticmethod
    def post(path, *args, **kwargs):
        if not path.endswith('/getwidgets') or 'json' not in kwargs or "searches" not in kwargs["json"]:
            return None

        query = get_nested_value(kwargs, ["json","searches",0,"q"])

        if not query:
            return None

        fname = query_to_filename(query)

        mock_response_file = f"supplier_laballey/response_data/POST__getwidgets__{fname}.json"

        return CurlRequestMocker(file=mock_response_file)

    @staticmethod
    def get(path, *args, **kwargs):
        if not path.endswith('/getwidgets') or "params" not in kwargs or "q" not in kwargs["params"]:
            return None

        query = get_nested_value(kwargs, ["params","q"])
        if not query:
            return None

        fname = query_to_filename(query)

        mock_response_file = f"supplier_laballey/response_data/GET__getwidgets__{fname}.json"

        return CurlRequestMocker(file=mock_response_file)
