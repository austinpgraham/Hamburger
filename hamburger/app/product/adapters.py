from pyramid.interfaces import IRequest

from zope import component
from zope import interface

from hamburger.dataserver.product.interfaces import IProduct

from hamburger.dataserver.product.model import HamProduct


@component.adapter(IRequest)
@interface.implementer(IProduct)
def _get_product_from_request(request):
    product = HamProduct.from_json(request.json)
    return product
