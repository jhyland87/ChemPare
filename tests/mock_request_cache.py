import os

from requests_cache import CachedSession
from requests_cache import FileCache


_cache_sessions = {}


def set_supplier_cache_session(supplier: str = "default"):
    if supplier not in _cache_sessions:
        save_to = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock_data", supplier)
        _cache_sessions[supplier] = CachedSession(
            cache_name=save_to,
            backend="filesystem",
            serializer="json",
            always_revalidate=False,
            urls_expire_after=None,
            expire_after=None,
            match_headers=True,
            stale_if_error=False,
        )
    return _cache_sessions.get(supplier)


__all__ = ["set_supplier_cache_session"]
