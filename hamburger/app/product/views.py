from pyramid.view import view_config

from pyramid.httpexceptions import HTTPOk
from pyramid.httpexceptions import HTTPConflict
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import exception_response

from zope import component

from hamburger.app import AbstractEditObjectView
from hamburger.app import AbstractResourceGetView
from hamburger.app import AbstractAuthenticatedView

from hamburger.app.product import PROVIDER
from hamburger.app.product import IDENTIFIER

from hamburger.dataserver.dataserver.interfaces import IDataserver

from hamburger.dataserver.product import AMOUNT
from hamburger.dataserver.product import USER_ID

from hamburger.dataserver.product.interfaces import IProduct
from hamburger.dataserver.product.interfaces import IProductCollection
from hamburger.dataserver.product.interfaces import IUserProductListCollection

from hamburger.dataserver.product.model import HamDonation

from hamburger.dataserver.provider.interfaces import IProvider
from hamburger.dataserver.provider.interfaces import IStripePayment


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
        appID = self.request.registry.settings.get("{}.appid".format(provider_name))
        if provider is None or appID is None:
            return HTTPBadRequest("Provider '{}' not found.".format(provider_name))
        product = provider.get_product(identifier, appID)
        if product is None:
            return HTTPBadRequest("Product '{}' could not be parsed.".format(identifier))
        if not self.context.insert(product):
            raise exception_response(409)
        return HTTPOk()


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


TOKEN = "token"


def _charge(donation, email):
    sp = component.getUtility(IStripePayment)
    return sp.charge(
        donation.token,
        donation.amount,
        "Donation to {}".format(donation.__parent__),
        email
    )


@view_config(context=IProduct,
             request_method="POST")
class DonateToView(AbstractAuthenticatedView):

    def __call__(self):
        # Check request body
        if AMOUNT not in self.request.json or\
           TOKEN not in self.request.json: # pragma: no cover
            return HTTPBadRequest()
        # Get info to pass to donations
        user_id = self.auth_user.username
        amount = float(self.request.json[AMOUNT])
        # Adjust the amount to be the remaining for the product
        if amount > self.context.total_donations:
            amount = int(round(self.context.price - self.context.total_donations))
        token = self.request.json[TOKEN]
        # Save the donation
        donation = HamDonation(userid=user_id, amount=amount, token=token)
        self.context[user_id] = donation
        # Charge the user
        result = _charge(donation, self.auth_user.email)
        if result.failure_code is not None: # pragma: no cover
            return exception_response(422, body={'error': 'Could not charge.'})
        return HTTPOk()


@view_config(context=IProduct)
class GetProductView(AbstractResourceGetView):
    pass


@view_config(context=IProductCollection)
class EditProductCollectionView(AbstractEditObjectView):
    pass
