from ebaysdk.finding import Connection

from zope import interface

from hamburger.dataserver.provider import AbstractProvider

from hamburger.dataserver.provider.interfaces import IProvider
from hamburger.dataserver.provider.interfaces import IEbayProvider
from hamburger.dataserver.provider.interfaces import IProductParser
from hamburger.dataserver.provider.interfaces import IProductFetcher

from hamburger.dataserver.product.model import HamProduct


@interface.implementer(IEbayProvider)
class EbayProvider(AbstractProvider):

    def get_product(self, identifier):
        self.fetcher.appID = self.appID
        return super(EbayProvider, self).get_product(identifier)


@interface.implementer(IProductFetcher)
class EbayFetcher():

    def fetch_product(self, identifier):
        self.api = Connection(appid=self.appID, config_file=None)
        args = {
            'keywords': identifier
        }
        response = self.api.execute('findItemsAdvanced', args)
        return response if response.reply.ack == "Success" else None


@interface.implementer(IProductParser)
class EbayParser():

    def parse_product(self, obj):
        items = obj.dict()['searchResult']['item']
        if len(items) <= 0:
            return None
        # Find item with minimum price
        sorted_items = sorted(items, key=lambda item: item['sellingStatus']['currentPrice']['value'], reverse=True)
        item = sorted_items.pop()
        product_args = {
            'title': item['title'],
            'hamid': "ham-ebay-{}".format(item['itemId']),
            'imageURL': item['galleryURL'] if 'galleryURL' in item else None,
            'itemURL': item['viewItemURL'],
            'price': float(item['sellingStatus']['currentPrice']['value'])
        }
        return HamProduct(**product_args)
