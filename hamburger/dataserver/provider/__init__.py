class AbstractProvider():

    def __init__(self, parser=None, fetcher=None, **kwargs):
        self.parser = parser
        self.fetcher = fetcher
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_product(self, identifier):
        result = self.fetcher.fetch_product(identifier)
        if result is None:
            return None # pragma: no cover
        return self.parser.parse_product(result)
