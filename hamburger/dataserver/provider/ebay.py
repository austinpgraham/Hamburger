from zope import interface

from hamburger.dataserver.provider import AbstractProvider

from hamburger.dataserver.provider.interfaces import IProvider
from hamburger.dataserver.provider.interfaces import IEbayProvider
from hamburger.dataserver.provider.interfaces import IProductParser
from hamburger.dataserver.provider.interfaces import IProductFetcher


@interface.implementer(IEbayProvider)
class EbayProvider(AbstractProvider):
    pass


@interface.implementer(IProductFetcher)
class EbayFetcher():

    def fetch_product(self, identifier):
        pass


@interface.implementer(IProductParser)
class EbayParser():

    def parse_product(self, obj):
        pass
