import pytest
from pytest_mock import MockerFixture
from curl_cffi import requests


def test_curl_cffi_get(mocker: MockerFixture):
    mock_get = mocker.patch("curl_cffi.requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "Mocked content"

    response = requests.get(
        "https://example.com", params=None, headers=None, cookies=None, auth=None, timeout=None, json=None, data=None
    )

    assert response.status_code == 200
    assert response.text == "Mocked content"
    mock_get.assert_called_once_with(
        "https://example.com", params=None, headers=None, cookies=None, auth=None, timeout=None, json=None, data=None
    )
