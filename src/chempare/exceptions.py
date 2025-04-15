class NoProductsFound(Exception):
    def __init__(self, supplier, query):
        self.supplier = supplier
        self.query = query

    def __str__(self):
        return f"No products found at supplier {self.supplier} for '{self.query}'"


class CaptchaEncountered(Exception):
    def __init__(self, supplier, query):
        self.supplier = supplier
        self.query = query

    def __str__(self):
        return f"Encountered a captcha when querying {self.supplier} for '{self.query}'"
