from pyramid.view import view_config

from pyramid.httpexceptions import HTTPForbidden

from hamburger.app import AbstractResourceGetView

from hamburger.dataserver.product.interfaces import IProductCollection


@view_config(context=IProductCollection)
class ProductCollectionView(AbstractResourceGetView):

    def __call__(self):
        if not self.context.is_public and self.auth_user.username != self.context.owner.username:
            token = self.request.json.get('access_token', None)
            if token is None or token != self.context.access_token:
                return HTTPForbidden()
        result = super(ProductCollectionView, self).__call__()
        return result
