from pyramid.view import view_config

from pyramid.httpexceptions import HTTPOk
from pyramid.httpexceptions import HTTPConflict
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPBadRequest

from zope import component

from hamburger.app import AbstractEditObjectView
from hamburger.app import AbstractResourceGetView
from hamburger.app import AbstractAuthenticatedView

from hamburger.app.product import PROVIDER
from hamburger.app.product import IDENTIFIER

from hamburger.dataserver.dataserver.interfaces import IDataserver

from hamburger.dataserver.product import USER_ID
from hamburger.dataserver.product import AMOUNT

from hamburger.dataserver.product.interfaces import IProduct
from hamburger.dataserver.product.interfaces import IProductCollection
from hamburger.dataserver.product.interfaces import IUserProductListCollection

from hamburger.dataserver.product.model import HamDonation

from hamburger.dataserver.provider.interfaces import IProvider


@view_config(context=IProductCollection)
class ProductCollectionView(AbstractResourceGetView):
    pass


@view_config(context=IProductCollection,
             request_method="POST",
             permission="edit")
class ProductPostView(AbstractAuthenticatedView):

    def __call__(self):
        if PROVIDER not in self.request.json or\
           IDENTIFIER not in self.request.json:
            return HTTPBadRequest()
        provider_name = self.request.json[PROVIDER]
        identifier = self.request.json[IDENTIFIER]
        provider = component.queryUtility(IProvider, name=provider_name, default=None)()
        if provider is None:
            return HTTPBadRequest("Provider '{}' not found.".format(provider_name))
        product = provider.get_product(identifier)
        if product is None:
            return HTTPBadRequest("Product '{}' could not be parsed.".format(identifier))
        return HTTPOk() if self.context.insert(product) else HTTPConflict()


@view_config(context=IDataserver,
             request_method="GET",
             name="providers",
             renderer="json")
class ProvidersGetView(AbstractAuthenticatedView):

    def __call__(self):
        if self.auth_user is None:
            return HTTPForbidden()
        providers = component.getUtilitiesFor(IProvider)
        return [p[0] for p in providers]


@view_config(context=IProduct,
             request_method="POST")
class DonateToView(AbstractAuthenticatedView):

    def __call__(self):
        if self.auth_user is None:
            return HTTPForbidden()
        if AMOUNT not in self.request.json:
            return HTTPBadRequest()
        user_id = self.auth_user.username
        amount = float(self.request.json[AMOUNT])
        donation = HamDonation(userid=user_id, amount=amount)
        self.context[user_id] = donation
        return HTTPOk()


@view_config(context=IProduct)
class GetProductView(AbstractResourceGetView):
    pass


@view_config(context=IProductCollection)
class EditProductCollectionView(AbstractEditObjectView):
    pass
