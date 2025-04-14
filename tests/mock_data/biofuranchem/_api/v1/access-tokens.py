from curl_cffi.requests.cookies import CookieTypes
from curl_cffi.requests.headers import HeaderTypes


cookies: CookieTypes = {
    "ssr-caching": "cache#desc=miss#varnish=miss_hit#dc#desc=fastly_g",
    "server-session-bind": "4f2e4f3d-1f14-4f30-bf61-302e6bd4a39b",
    "XSRF-TOKEN": "1744556905|R-oTMgt-72X9",
    "client-session-bind": "4f2e4f3d-1f14-4f30-bf61-302e6bd4a39b",
    "hs": "-1419956954",
    "svSession": "18dae800ca5da5575b8bf8ad3bafab84a474e389022b195e17958119d6b91d1a2b5652d1f26f42c0abc09a1eb6c9ad271e60994d53964e647acf431e4f798bcd3a4d47fbe941312dbe665d754d5b8c426a1d64f28a63d1213c8808c3b7bfe0eda6c2028264e3552acdee1c375c0b8f21c8b26bd20f8b0acbd067c030aba8e8553446555bdb3c443e6ebbb1aa16b781f1",
}
headers: HeaderTypes = {
    "content-type": "application/json; charset=utf-8",
    "access-control-allow-origin": "*",
    "strict-transport-security": "max-age=86400",
    "age": "178838",
    "x-wix-request-id": "1744556916.96756475281053839353",
    "set-cookie": "hs=-1419956954; Path=/; Domain=www.biofuranchem.com; Secure; HTTPOnly, svSession=18dae800ca5da5575b8bf8ad3bafab84a474e389022b195e17958119d6b91d1a2b5652d1f26f42c0abc09a1eb6c9ad271e60994d53964e647acf431e4f798bcd3a4d47fbe941312dbe665d754d5b8c426a1d64f28a63d1213c8808c3b7bfe0eda6c2028264e3552acdee1c375c0b8f21c8b26bd20f8b0acbd067c030aba8e8553446555bdb3c443e6ebbb1aa16b781f1; Max-Age=63072000; Expires=Tue, 13 Apr 2027 15:08:36 GMT; Path=/; Domain=www.biofuranchem.com; Secure; HTTPOnly; SameSite=None, client-session-bind=4f2e4f3d-1f14-4f30-bf61-302e6bd4a39b; Path=/; Secure; SameSite=Lax;, server-session-bind=4f2e4f3d-1f14-4f30-bf61-302e6bd4a39b; Path=/; Secure; SameSite=Lax; HttpOnly;",
    "cache-control": "private,no-cache,no-store",
    "server": "Pepyaka",
    "x-content-type-options": "nosniff",
    "content-encoding": "br",
    "accept-ranges": "bytes",
    "date": "Sun, 13 Apr 2025 15:08:37 GMT",
    "x-served-by": "cache-bur-kbur8200063-BUR",
    "x-cache": "MISS",
    "vary": "Accept-Encoding",
    "server-timing": "cache;desc=hit, varnish;desc=hit_miss, dc;desc=fastly_uw2-pub-1_g",
    "x-seen-by": "yvSunuo/8ld62ehjr5B7kA==,9WD8GAcpJgs/Ng1WkD2i0h9slopJdhD+WySraMrpIY8=,m0j2EEknGIVUW/liY8BLLt4IRtmbVvKklG4Zpf3E4eIG/hKs8AeY1T4OIbgnD+yx,2d58ifebGbosy5xc+FRaluGoKNqZFFgjbsWjf36h3JPX4Tzd14TkZSlnzn0mDSdwMYEe81QB7oq04x/mNpwrMw==,2UNV7KOq4oGjA5+PKsX47J3r+lLfYYyxvx/JoKUHfidjPZTuGyYqVhtmEIgJUb4w",
    "via": "1.1 google",
    "glb-x-seen-by": "bS8wRlGzu0Hc+WrYuHB8QIg44yfcdCMJRkBoQ1h6Vjc=",
    "alt-svc": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000",
}
json_content = {
    "hs": -1143048074,
    "visitorId": "5e5c4265-9c50-4627-ac5e-754a1eef5939",
    "svSession": "a66a6a212d566f1ec32513b561eaeaff346069567559d4f41a6df099caf6164dc939fbee7b54e7921130b8c7710732b41e60994d53964e647acf431e4f798bcd6f0595cc6f10cc0ef9a4af86ed9cdbb5967222868dcae6df2540ad54a03b8f50a6c2028264e3552acdee1c375c0b8f21c8b26bd20f8b0acbd067c030aba8e8553446555bdb3c443e6ebbb1aa16b781f1",
    "ctToken": "dW1RSmtJRHJWc21DazF1OFRjNEZaUDR4QTJoeXktTV9UVWlfZ3FUZ1RFQXx7InVzZXJBZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMzMuMC4wLjAgU2FmYXJpLzUzNy4zNiIsInZhbGlkVGhyb3VnaCI6MTc0NTE2MTgzMzY2Nn0",
    "mediaAuthToken": "eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcHA6MTEyNjU1MzUxNDEyMDM1MiIsInN1YiI6InNpdGU6MTFmYjQ5ZGYtYjA0OC00YzdjLWI0YjYtYWRmNTc1MGZmZWE4IiwiYXVkIjoidXJuOnNlcnZpY2U6ZmlsZS51cGxvYWQiLCJleHAiOjE3NDQ2NDM0MzMsImlhdCI6MTc0NDU1NzAzMywianRpIjoiOHBVNDhyRUtsa1IzSDNnUFRHVUh2dyIsImFkZGVkQnkiOiJhbm9ueW1vdXM6NWU1YzQyNjUtOWM1MC00NjI3LWFjNWUtNzU0YTFlZWY1OTM5In0.2XwN1xWVrxMQvi7hNftMJJbfLju5Z0kR-yqvr5Br_Gw",
    "apps": {
        "1380b703-ce81-ff05-f115-39571d94dfcd": {
            "instance": "6-FAjE-qJcEANebpKDvxfljnNwaybv5SF7mjUF-Djms.eyJpbnN0YW5jZUlkIjoiMjI1N2U2ODMtNjg2Yy00NjRkLTkzMTAtMjVmZTNjMjRlN2Q0IiwiYXBwRGVmSWQiOiIxMzgwYjcwMy1jZTgxLWZmMDUtZjExNS0zOTU3MWQ5NGRmY2QiLCJtZXRhU2l0ZUlkIjoiMTFmYjQ5ZGYtYjA0OC00YzdjLWI0YjYtYWRmNTc1MGZmZWE4Iiwic2lnbkRhdGUiOiIyMDI1LTA0LTEzVDE1OjEwOjMzLjY2NloiLCJ2ZW5kb3JQcm9kdWN0SWQiOiJzdG9yZXNfc2lsdmVyIiwiZGVtb01vZGUiOmZhbHNlLCJvcmlnaW5JbnN0YW5jZUlkIjoiMDc5ZjFlMmItMWNlZi00ZWY1LWJlN2QtODcwYjc4NDNkMTI5IiwiYWlkIjoiNWU1YzQyNjUtOWM1MC00NjI3LWFjNWUtNzU0YTFlZWY1OTM5IiwiYmlUb2tlbiI6IjMzYWNhZjVjLWQ4MjQtMGEzMS0yN2E2LTg4MGI0OTJiMTk3YyIsInNpdGVPd25lcklkIjoiNzhkZGE4YmUtZTEyMi00MmE5LWI3NzItZmVjYTk1NDRmZDA4IiwiYnMiOiJvXzJkY1RIN3VrblQ3Z3FVeFNJUnVNcXk2R2FiQWpzbGFOeGpUem1OWGhFLklqZGxaV1UzTVRZNExUVXlNRFF0TkdRNE5pMDVObUl5TFRBME5tWXhZMkpsT0dRMlppSSIsInNjZCI6IjIwMjItMDEtMDJUMjA6MjE6NDcuMTU4WiJ9",
            "intId": 1952,
        }
    },
}


__all__ = ["headers", "cookies", "json_content"]
