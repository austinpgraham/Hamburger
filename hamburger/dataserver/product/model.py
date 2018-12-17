from DateTime import DateTime

from random import randint

from pyramid.security import Allow
from pyramid.security import Authenticated

from zope import interface

from hamburger.dataserver.dataserver.model import Contained
from hamburger.dataserver.dataserver.model import Collection

from hamburger.dataserver.product.interfaces import IProduct
from hamburger.dataserver.product.interfaces import IProductCollection
from hamburger.dataserver.product.interfaces import IUserProductListCollection


@interface.implementer(IProduct)
class HamProduct(Contained):
    __key__ = "hamid"
    __acl__ = [
        (Allow, Authenticated, "view"),
    ]

    KEYS = [
        "hamid",
        "title",
        "brand",
        "price"
    ]

    def _gen_id(self):
        _hashstr = self.brand.replace(" ", "")+self.title.replace(" ", "")
        return hash(_hashstr)

    def __init__(self, hamid=None, title=None,
                 brand=None, price=None):
        self.title = title
        self.brand = brand
        self.price = price
        self.hamid = hamid if hamid is not None else self._gen_id()


@interface.implementer(IProductCollection)
class HamProductCollection(Collection):
    __name__ = "products"
    __acl__ = [
        (Allow, Authenticated, "edit"),
    ]

    def _prevent_collision(self, new_obj):
        while new_obj.hamid in self:
            new_obj.hamid += str(randint(00000, 99999))

    def insert(self, new_obj, check_member=False):
        if not IProduct.providedBy(new_obj):
            raise ValueError("Cannot add non-IProduct to IProductCollection")
        self._prevent_collision(new_obj)
        return super(HamProductCollection, self).insert(new_obj, check_member=check_member)


@interface.implementer(IUserProductListCollection)
class HamUserProductListCollection(Collection):
    __name__ = "products"

    def __init__(self, title=None, is_public=False):
        self.title = title
        self.is_public = is_public
        self.created_at = DateTime()

    def insert(self, new_obj, check_member=False):
        if not IProductCollection.providedBy(new_obj):
            raise ValueError("Cannot add non-IProductCollection to IUserProductListCollection")
        return super(HamUserProductListCollection, self).insert(new_obj, check_member=check_member)
