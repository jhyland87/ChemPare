"""Common Exceptions module"""


class NoProductsFound(Exception):
    """
    Raised when the supplier returns no products

    Attributes:
        supplier (str): Name of supplier.
        query (str): String queried for.
    """

    def __init__(self, supplier: str, query: str):
        """
        Initializes the NoProductsFound exception

        Args:
            supplier (str): Name of supplier.
            query (str): String queried for.
        """

        self.supplier = supplier
        self.query = query

    def __str__(self):
        return f"No products found at supplier {self.supplier} for '{self.query}'"


class CaptchaEncountered(Exception):
    """
    Raised when the HTTP request to a supplier website encounters a captcha/firewall

    Attributes:
        supplier (str): Name of supplier.
        url (str): URL the captcha was encountered at.
        captcha_type (str | None, optional): Cloudflare, Datadome, etc. (optional)
    """

    def __init__(self, supplier: str, url: str, captcha_type: str | None = None):
        """
        Initializes the CaptchaEncountered exception

        Args:
            supplier (str): Name of supplier.
            url (str):  URL the captcha was encountered at.
            captcha_type (str | None, optional): Cloudflare, Datadome, etc. Defaults to None.
        """
        self.supplier = supplier
        self.url = url
        self.captcha_type = captcha_type

    def __str__(self):
        return f"Encountered a captcha when querying supplier {self.supplier} at address {self.url}"


class NoMockDataFound(Exception):
    """
    Raised when a unit test is triggered but finds no local mock data

    Attributes:
        url (str): URL the unit test called.
    """

    def __init__(self, url: str):
        """
        Initializes the NoMockDataFound exception

        Args:
            url (str): URL the unit test called.
        """
        self.url = url

    def __str__(self):
        return f"No mock data found when querying URL {self.url}"
