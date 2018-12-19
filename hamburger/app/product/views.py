from pyramid.view import view_config

from pyramid.httpexceptions import HTTPOk
from pyramid.httpexceptions import HTTPConflict
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPBadRequest

from hamburger.app import AbstractResourceGetView
from hamburger.app import AbstractAuthenticatedView

from hamburger.dataserver.product.interfaces import IProduct
from hamburger.dataserver.product.interfaces import IProductCollection


@view_config(context=IProductCollection)
class ProductCollectionView(AbstractResourceGetView):
    pass


@view_config(context=IProductCollection,
             request_method="POST",
             permission="edit")
class ProductPostView(AbstractAuthenticatedView):

    def __call__(self):
        if 'hamid' not in self.request.json:
            return HTTPBadRequest()
        data = self.request.json
        data['hamid'] = data['hamid'] if data['hamid'] != "" else None
        self.request.json = data
        item = IProduct(self.request)
        if item is None:
            return HTTPBadRequest()
        if not self.context.insert(item):
            return HTTPConflict()
        return HTTPOk()
