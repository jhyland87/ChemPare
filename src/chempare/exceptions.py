class NoProductsFound(Exception):
    def __init__(self, supplier, query):
        self.supplier = supplier
        self.query = query

    def __str__(self):
        return f"No products found at supplier {self.supplier} for '{self.query}'"


class CaptchaEncountered(Exception):
    def __init__(self, supplier, url, captcha_type=None):
        self.supplier = supplier
        self.url = url
        self.captcha_type = captcha_type

    def __str__(self):
        return f"Encountered a captcha when querying supplier {self.supplier} at address {self.url}"


class NoMockDataFound(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return f"No mock data found when querying URL {self.url}"
