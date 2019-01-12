from zope import interface

from zope.schema import Text
from zope.schema import Object


class IProductFetcher(interface.Interface):
    """
    Provides functions to fetch a product from a given
    provider.
    """

    def fetch_product(identifier):
        """
        Fetch a product with a given identifier.
        """


class IProductParser(interface.Interface):
    """
    Takes results from a fetch and parses into 
    a product instance.
    """

    def parse_product(obj):
        """
        Parse the given product object.
        """


class IProvider(interface.Interface):
    """
    A marker interface for a class that provides details
    on how to retrieve data from a given provider.
    """
    fetcher = Object(IProductFetcher,
                     title="Product Fetcher",
                     required=True)

    parser = Object(IProductParser,
                    title="Product Parser",
                    required=True)

    def get_product(identifier):
        """
        Returns an IProduct from a given identifier.
        """


class IEbayProvider(IProvider):
    """
    Marker of the Ebay provider class.
    """

    appID = Text(title="Ebay Registered App ID",
                 required=True)


class IStripePayment(interface.Interface):
    """
    Marker interface for stripe payment
    """
    sk = Text(title="Secret Key",
              required=True)

    def charge(token, amount, description, email):
        """
        Charge the given amount for the transaction
        """

    def refund(token, partial=None):
        """
        Refund the given charge amount.
        """
