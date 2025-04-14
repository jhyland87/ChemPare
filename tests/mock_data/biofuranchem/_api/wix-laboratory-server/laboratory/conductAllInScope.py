from curl_cffi.requests.cookies import CookieTypes
from curl_cffi.requests.headers import HeaderTypes


cookies: CookieTypes = {
    "server-session-bind": "c34892b5-e564-49e1-b482-0f49101ca7ca",
    "ssr-caching": "cache#desc=hit#varnish=hit_miss#dc#desc=fastly_uw2-pub-1_g",
    "XSRF-TOKEN": "1744556664|vNliiTojvItF",
}

headers: HeaderTypes = {
    "content-type": "application/json;charset=utf-8",
    "expires": "Thu, 01 Jan 1970 00:00:00 GMT",
    "cache-control": "no-cache",
    "x-wix-request-id": "1744556664.05756436541924081323, 1744556664.05756436541924081323",
    "set-cookie": "_wixAB3=1292391#1|4195310#1; Max-Age=15724800; Expires=Sun, 12 Oct 2025 15:04:24 GMT; Path=/_api/wix-laboratory-server/laboratory/conductAllInScope; Domain=.wix.com, XSRF-TOKEN=1744556664|vNliiTojvItF; Path=/; Domain=www.biofuranchem.com; Secure; SameSite=None",
    "server": "Pepyaka",
    "x-content-type-options": "nosniff",
    "content-encoding": "br",
    "accept-ranges": "bytes",
    "date": "Sun, 13 Apr 2025 15:04:24 GMT",
    "x-served-by": "cache-bur-kbur8200027-BUR",
    "x-cache": "MISS",
    "vary": "Accept-Encoding",
    "x-seen-by": "yvSunuo/8ld62ehjr5B7kA==,1ev8u3tblITHmgXkyGXE9h9slopJdhD+WySraMrpIY8=,m0j2EEknGIVUW/liY8BLLo8CJZFp5+V7VR/WYDn10bQG/hKs8AeY1T4OIbgnD+yx,jdDt270t0fniy2BugWKBrVVANJM5P6S4TWxDzGn3H9YOIv81siZFFg8Zg0+ti17jUrfzQvSH9/TeaE9PK5K3CQ==,R8nVwPJv9QJL1m78OROO+EOuTTPRBBS++PRaxs794ZE=,mvxQ9qSAmY38asKjFCcmGxT5VqlepTTMTa3jctupN0kV+pU3RmQcSauZPlBhv+ivC4NMJLc21zHz+aWgzZO5VCowlimqXXRZThBA8XBqMGs=",
    "via": "1.1 google",
    "glb-x-seen-by": "bS8wRlGzu0Hc+WrYuHB8QIg44yfcdCMJRkBoQ1h6Vjc=",
    "alt-svc": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000",
}


__all__ = ["heaaders", "cookies"]
