from DateTime import DateTime

from random import randint

from pyramid.security import Deny
from pyramid.security import Allow
from pyramid.security import Everyone
from pyramid.security import Authenticated

from zope import interface

from hamburger.dataserver.dataserver.model import Contained
from hamburger.dataserver.dataserver.model import Collection

from hamburger.dataserver.product.interfaces import IProduct
from hamburger.dataserver.product.interfaces import IDonation
from hamburger.dataserver.product.interfaces import IProductCollection
from hamburger.dataserver.product.interfaces import IDonationCollection
from hamburger.dataserver.product.interfaces import IUserProductListCollection


@interface.implementer(IDonationCollection)
class HamDonationCollection(Collection):
    __name__ = "donations"

    def insert(self, new_obj, check_member=False):
        if not IDonation.providedBy(new_obj):
            raise ValueError("Cannot add non-IDonation to IDonationCollection")
        return super(HamDonationCollection, self).insert(new_obj, check_member=check_member)


@interface.implementer(IDonation)
class HamDonation(Contained):
    __key__ = "userid"
    # TODO: DETERMINE ACCESS RIGHTS FOR THIS OBJECT
    __acl__ = []

    # TODO" Is this externalizable?
    KEYS = []

    def __init__(self, userid=None, amount=None, token=None):
        self.userid = userid
        self.amount = amount
        self.token = token


@interface.implementer(IProduct)
class HamProduct(Contained):
    __key__ = "hamid"
    __acl__ = [
        (Allow, Authenticated, "view"),
    ]

    KEYS = [
        'title',
        'price',
        'itemURL',
        'imageURL',
        'hamid'
    ]

    def __init__(self, hamid=None, title=None,
                 itemURL=None, imageURL=None, price=None):
        self.title = title
        self.price = price
        self.itemURL = itemURL
        self.imageURL = imageURL
        self.hamid = hamid
        self._donations = HamDonationCollection()

    def __getitem__(self, key):
        if key not in self._donations:
            raise KeyError("{} not in {}'s donation list.".format(key, self.hamid))
        return self._donations[key]

    def __setitem__(self, key, obj):
        self._donations.insert(obj)

    def __contains__(self, val):
        return val in self._donations

    def __acl__(self):
        return []

    def to_json(self, request):
        result = super(HamProduct, self).to_json(request)
        result['total_donations'] = self.total_donations
        return result

    @property
    def total_donations(self):
        return sum([self._donations[x].amount for x in self._donations])


@interface.implementer(IProductCollection)
class HamProductCollection(Collection, Contained):
    __key__ = "title"

    KEYS = [
        "title",
        "is_public",
        "created_at",
        "access_token"
    ]

    def _gen_token(self):
        return hash(self.title + str(randint(00000, 99999)))

    def __init__(self, title=None, is_public=False):
        super(HamProductCollection, self).__init__()
        self.title = title
        self.__name__ = self.title
        self.is_public = is_public
        self.created_at = DateTime()
        self.access_token = "" if is_public else self._gen_token()

    def insert(self, new_obj, check_member=True):
        if not IProduct.providedBy(new_obj):
            raise ValueError("Cannot add non-IProduct to IProductCollection")
        return super(HamProductCollection, self).insert(new_obj, check_member=check_member)

    def to_json(self, request):
        result = super(HamProductCollection, self).to_json(request)
        permissions = getattr(self, 'permissions', None)
        if permissions is not None:
            result['permissions'] = permissions
        result['created_at'] = str(result['created_at'])
        return result

    @property
    def owner(self):
        return self.__parent__.__parent__

    @property
    def __acl__(self):
        perms = [(Allow, self.owner.username, "edit")]
        if self.is_public:
            perms.append((Allow, Authenticated, "view"))
        else:
            perms.extend([(Allow, self.owner.username, "view"), (Deny, Everyone, "view")])
        return perms


@interface.implementer(IUserProductListCollection)
class HamUserProductListCollection(Collection):
    __name__ = "wishlists"

    def insert(self, new_obj, check_member=False):
        if not IProductCollection.providedBy(new_obj):
            raise ValueError("Cannot add non-IProductCollection to IUserProductListCollection")
        return super(HamUserProductListCollection, self).insert(new_obj, check_member=check_member)
