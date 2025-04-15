class NoProductsFound(Exception):
    def __init__(self, supplier, query):
        self.supplier = supplier
        self.query = query

    def __str__(self):
        return f"No products found at supplier {self.supplier} for query {self.query}"


class NoProductsFound(Exception):
    def __init__(self, supplier, query):
        self.supplier = supplier
        self.query = query

    def __str__(self):
        return f"No products found at supplier {self.supplier} for query {self.query}"
