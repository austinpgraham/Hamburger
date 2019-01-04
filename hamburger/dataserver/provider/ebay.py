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
    pass


@interface.implementer(IProductFetcher)
class EbayFetcher():

    def __init__(self):
        self.appID = "AustinGr-Hamburge-PRD-660b9b3c7-a4f8c441"
        self.api = Connection(appid=self.appID, config_file=None)

    def fetch_product(self, identifier):
        arg = '<productId type="ReferenceID">{}</productId>'.format(int(identifier))
        response = self.api.execute('findItemsByProduct', arg)
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
            'price': item['sellingStatus']['currentPrice']['value']
        }
        return HamProduct(**product_args)
