import os

from requests_cache import CachedSession
from requests_cache import FileCache


_cache_sessions = {}

requests = None


def set_supplier_cache_session(supplier: str = "default"):
    if supplier not in _cache_sessions:
        print(f"Supplier ${supplier} does not have a mock_data directory - creating it")
        save_to = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock_data", supplier)
        _cache_sessions[supplier] = CachedSession(
            cache_name=save_to,
            backend="filesystem",
            serializer="json",
            ignored_parameters=(
                'Authorization',
                "session-1",
                "session-2",
                "session-3",
                "session-4",
                "session-5",
                'X-API-KEY',
                'access_token',
                "Content-Length",
                "created_at",
                'api_key',
                "Alt-Svc",
                "client-session-bind",
                "session-session-bind",
                "age",
                "date",
                "Set-Cookie",
                "ssr-caching",
                "Expires",
                "etag",
                "glb-x-seen-by",
                "x-seen-by",
                "x-served-by",
                "x-wix-request-id",
            ),
            always_revalidate=False,
            urls_expire_after=None,
            expire_after=None,
            allowable_methods=['POST', 'PUT', 'GET', 'HEAD'],
            allowable_codes=[
                100,
                200,
                201,
                202,
                204,
                206,
                301,
                302,
                304,
                307,
                308,
                400,
                401,
                402,
                403,
                404,
                405,
                406,
                408,
                414,
                429,
                500,
                502,
                503,
                504,
            ],
            match_headers=False,
            stale_if_error=False,
        )
    return _cache_sessions.get(supplier)


#   "headers": {
#     "Alt-Svc": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000",
#     "Transfer-Encoding": "chunked",
#     "accept-ranges": "bytes",
#     "age": "46844",
#     "cache-control": "public,max-age=0,must-revalidate",
#     "content-encoding": "gzip",
#     "content-type": "application/json;charset=utf-8",
#     "date": "Fri, 18 Apr 2025 03:34:55 GMT",
#     "etag": "W/\"c125cdd132588fd8187b8363cecac4d7\"",
#     "glb-x-seen-by": "bS8wRlGzu0Hc+WrYuHB8QIg44yfcdCMJRkBoQ1h6Vjc=",
#     "server": "Pepyaka",
#     "server-timing": "cache;desc=miss, varnish;desc=miss_hit, dc;desc=fastly_g",
#     "vary": "Accept-Encoding",
#     "via": "1.1 google",
#     "x-cache": "HIT",
#     "x-content-type-options": "nosniff",
#     "x-seen-by": "yvSunuo/8ld62ehjr5B7kA==,xIKq3IotbbLp4+7DTTMx8R9slopJdhD+WySraMrpIY8=,m0j2EEknGIVUW/liY8BLLrqaBeSD0wx65EKugKS/8wEG/hKs8AeY1T4OIbgnD+yx,2d58ifebGbosy5xc+FRalk25wcj4f/HxjmCi8xvEklfvkHmq5HJsAm1DeVKOuabLY+p2VGTQAonQ0tncu0K/Dw==,2UNV7KOq4oGjA5+PKsX47NoP9ImTZp7EGowz+sg6PHMG/hKs8AeY1T4OIbgnD+yx,R8nVwPJv9QJL1m78OROO+EOuTTPRBBS++PRaxs794ZE=",
#     "x-served-by": "cache-bur-kbur8200146-BUR",
#     "x-wix-request-id": "1744947295.384991498155657863"
#   },

__all__ = ["set_supplier_cache_session", "requests"]
