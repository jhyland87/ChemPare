import os
from http import HTTPMethod
from http import HTTPStatus

from requests_cache import CachedSession

from chempare.utils import utils


_cache_sessions = {}

requests = None


# print(f"{save_responses=}")


def set_supplier_cache_session(supplier: str = "default"):

    # called_from_test = utils.getenv("CALLED_FROM_TEST", False)
    # test_monkeypatching = utils.getenv("TEST_MONKEYPATCHING", False)
    # print(f"{test_monkeypatching=}, {called_from_test=}")

    force_refresh = utils.getenv("PYTEST_FORCE_REFRESH", False)
    only_mock = utils.getenv("PYTEST_ONLY_MOCK_DATA", True)

    print(f"{force_refresh=}, {force_refresh=}")

    if supplier not in _cache_sessions:
        save_to = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock_data", supplier)

        _cache_sessions[supplier] = CachedSession(
            cache_name=save_to,
            only_if_cached=only_mock,
            force_refresh=force_refresh,
            backend="filesystem",
            serializer="json",
            always_revalidate=False,
            cache_control=False,
            urls_expire_after=None,
            expire_after=None,
            allowable_methods=[
                HTTPMethod.POST,
                HTTPMethod.GET,
                HTTPMethod.HEAD,
                HTTPMethod.OPTIONS,
                HTTPMethod.CONNECT,
            ],
            allowable_codes=[
                HTTPStatus.CONTINUE,
                HTTPStatus.OK,
                HTTPStatus.NO_CONTENT,
                HTTPStatus.PARTIAL_CONTENT,
                HTTPStatus.FOUND,
                HTTPStatus.NOT_MODIFIED,
                HTTPStatus.USE_PROXY,
                HTTPStatus.TEMPORARY_REDIRECT,
                HTTPStatus.PERMANENT_REDIRECT,
                HTTPStatus.BAD_REQUEST,
                HTTPStatus.UNAUTHORIZED,
                HTTPStatus.FORBIDDEN,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.METHOD_NOT_ALLOWED,
                HTTPStatus.NOT_ACCEPTABLE,
                HTTPStatus.PROXY_AUTHENTICATION_REQUIRED,
                HTTPStatus.REQUEST_TIMEOUT,
                HTTPStatus.CONFLICT,
                HTTPStatus.GONE,
                HTTPStatus.PRECONDITION_FAILED,
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                HTTPStatus.REQUEST_URI_TOO_LONG,
                HTTPStatus.TOO_MANY_REQUESTS,
                HTTPStatus.UNAVAILABLE_FOR_LEGAL_REASONS,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                HTTPStatus.NOT_IMPLEMENTED,
                HTTPStatus.BAD_GATEWAY,
                HTTPStatus.SERVICE_UNAVAILABLE,
                HTTPStatus.HTTP_VERSION_NOT_SUPPORTED,
                HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED,
            ],
            match_headers=False,
            stale_if_error=False,
        )
    return _cache_sessions.get(supplier)


__all__ = ["set_supplier_cache_session", "requests"]
