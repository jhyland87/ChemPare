
from tests.mock_data.curl_request_mocker import query_to_filename
from tests.mock_data.curl_request_mocker import get_nested_value
from tests.mock_data.curl_request_mocker import CurlRequestMocker


class curl_cffi:
    @staticmethod
    def post(path, *args, **kwargs):
        if not path.endswith('/multi_search') or 'json' not in kwargs or "searches" not in kwargs["json"]:
            return None

        query = get_nested_value(kwargs, ["json","searches",0,"q"])

        if not query:
            return None

        fname = query_to_filename(query)

        mock_response_file = f"supplier_chemsavers/response_data/POST__multi_search__{fname}.json"

        return CurlRequestMocker(file=mock_response_file)

    @staticmethod
    def get(path, *args, **kwargs):
        pass
