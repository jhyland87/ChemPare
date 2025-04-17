import os

from requests_cache import CachedSession
from requests_cache import FileCache


mock_cfg = None

CWD = os.path.dirname(os.path.abspath(__file__))

_cache_sessions = {}


requests = None


def set_supplier_cache_session(supplier: str = 'default'):
    if supplier not in _cache_sessions:
        _cache_sessions[supplier] = CachedSession(
            cache_name=f'{CWD}/{supplier}',
            backend='filesystem',
            serializer='json',
            always_revalidate=False,
            urls_expire_after=None,
            expire_after=None,
            match_headers=True,
            stale_if_error=False,
        )
    return _cache_sessions.get(supplier)


# # cache_name, backend, serializer, expire_after, urls_expire_after, always_revalidate, match_headers, stale_if_error,
# session = CachedSession(
#     cache_name=f'{CWD}/mock-request-cache-data',
#     backend='filesystem',
#     serializer='json',
#     always_revalidate=False,
#     urls_expire_after=None,
#     expire_after=None,
#     match_headers=True,
#     stale_if_error=False,
# )


__all__ = ["requests"]
