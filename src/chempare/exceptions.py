"""Common Exceptions module"""
from __future__ import annotations


class NoProductsFoundError(Exception):
    """
    Raised when the supplier returns no products

    Attributes:
        supplier (str): Name of supplier.
        query (str): String queried for.
    """

    def __init__(self, supplier: str, query: str) -> None:
        """
        Initializes the NoProductsFoundError exception

        Args:
            supplier (str): Name of supplier.
            query (str): String queried for.
        """
        self.supplier = supplier
        self.query = query
        self.message = (
            "No products found at supplier {supplier} for '{query}'"
        ).format_map(self.__dict__)

        super(NoProductsFoundError, self).__init__(self.message)


class CaptchaError(Exception):
    """
    Raised when the HTTP request to a supplier website encounters a captcha/firewall

    Attributes:
        supplier (str): Name of supplier.
        url (str): URL the captcha was encountered at.
        captcha_type (str | None, optional): Cloudflare, Datadome, etc. (optional)
    """

    def __init__(self, supplier: str, url: str, captcha_type: str | None = None) -> None:
        """
        Initializes the CaptchaError exception

        Args:
            supplier (str): Name of supplier.
            url (str):  URL the captcha was encountered at.
            captcha_type (str | None, optional): Cloudflare, Datadome, etc. Defaults to None.
        """
        self.supplier = supplier
        self.url = url
        self.captcha_type = captcha_type
        self.message = (
            "Captcha encountered for {supplier} at address {url}"
        ).format_map(self.__dict__)

        super(CaptchaError, self).__init__(self.message)


class NoMockDataError(Exception):
    """
    Raised when a unit test is triggered but finds no local mock data

    Attributes:
        url (str): URL the unit test called.
        supplier (str | None, optional): Supplier module/name. Defaults to None.
        details (str | None, optional): Optional string with any extra details. Defaults to None.
    """

    def __init__(self, url: str, supplier: str | None = None, details: str | None = None) -> None:
        """
        Initializes the NoMockDataError exception

        Args:
            url (str): URL the unit test called.
            supplier (str | None, optional): Supplier module/name. Defaults to None.
            details (str | None, optional): Optional string with any extra details.
        """
        self.url = url
        self.details = details
        self.supplier = supplier
        self.message = (
            "No mock data found when querying URL {url} - {details}"
        ).format_map(self.__dict__)

        super(NoMockDataError, self).__init__(self.message)


class ProductListQueryError(Exception):
    def __init__(self, url: str, supplier: str):
        """
        Initializes the NoMockDataError exception

        Args:
            url (str): URL the unit test called.
            supplier (str | None, optional): Supplier module/name. Defaults to None.
        """
        self.url = url
        self.supplier = supplier
        self.message = (
            "Initial request for products list from {supplier} returned falsy - {url}"
        ).format_map(self.__dict__)

        super(ProductListQueryError, self).__init__(self.message)


# class ParsingProductHtmlError(Exception):
#     def __init__(
#         self,
#         message: str | None = None,
#         error: Exception | None = None,
#         supplier: str | None = None,
#         url: str | None = None,
#     ) -> None:
#         self.message = message or "Error parsing product page"
#         self.error = error
#         self.supplier = supplier
#         self.url = url

#         super(ParsingProductHtmlError, self).__init__(self.message)


class UnsupportedPlatformError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

        super(UnsupportedPlatformError, self).__init__(self.message)
