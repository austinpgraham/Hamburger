class AbstractProvider():

    def __init__(self, parser=None, fetcher=None):
        self.parser = parser
        self.fetcher = fetcher

    def get_product(identifier):
        result = self.fetcher.fetch_product(identifier)
        if result is None:
            return None
        return self.parser.parse_product(result)
