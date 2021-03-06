import copy
import time

from zope import interface
from zope import component

from pyramid.security import Allow
from pyramid.security import forget
from pyramid.security import remember
from pyramid.security import Everyone
from pyramid.security import Authenticated

from hamburger.dataserver.user.interfaces import IUser
from hamburger.dataserver.user.interfaces import IAuthedUser
from hamburger.dataserver.user.interfaces import IGoogleUser
from hamburger.dataserver.user.interfaces import IFacebookUser
from hamburger.dataserver.user.interfaces import IUserCollection
from hamburger.dataserver.user.interfaces import IPermissionCollection

from hamburger.dataserver.product.model import HamUserProductListCollection

from hamburger.dataserver.dataserver.interfaces import IRedundancyCheck

from hamburger.dataserver.dataserver.adapters import to_external_object

from hamburger.dataserver.dataserver.model import Contained
from hamburger.dataserver.dataserver.model import Collection

from hamburger.dataserver.dataserver.security import get_hash
from hamburger.dataserver.dataserver.security import check_hash


@interface.implementer(IUser)
class HamUser(Contained):

    __key__ = "username"

    KEYS = [
        'username',
        'first_name',
        'last_name',
        'email',
        'password',
        'profile_pic',
        'phone_number'
    ]

    EXCLUDE = [
        'password',
    ]

    def __init__(self, username=None, first_name=None,
                 last_name=None, email=None,
                 password=None, phone_number=None,
                 profile_pic=""):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.profile_pic = profile_pic
        self._lists = HamUserProductListCollection()
        self._lists.__parent__ = self

    def authenticate(self, password, request):
        if check_hash(password, self.password):
            return remember(request, self.get_key())
        return None # pragma: no cover

    def deauthenticate(self, request):
        return forget(request) # pragma: no cover

    def check_auth(self):
        return self

    def is_empty(self):
        return self.username is None

    def __getitem__(self, key):
        if key not in self._lists:
            raise KeyError("{} not in {}'s collection.".format(key, self.username))
        return self._lists[key]

    def __setitem__(self, key, obj):
        self._lists.insert(obj, check_member=True)

    def __contains__(self, val):
        return val in self._lists

    def to_json(self, request, authed_user=None):
        result = super(HamUser, self).to_json(request)
        authed_user = authed_user if authed_user is not None else IAuthedUser(request)
        # This is causing write conflicts in ZODB.
        # Should be first on the list to fix along with handles
        # on ZODB write conflicts themselves.
        lists = copy.deepcopy(self._lists)
        for _list in lists:
            _list = lists[_list]
            permissions = component.queryMultiAdapter((authed_user, _list), IPermissionCollection)
            _list.permissions = permissions
        result['wishlists'] = to_external_object(lists, request)
        return result

    @property
    def __acl__(self):
        return [
            (Allow, Authenticated, "view"),
            (Allow, self.username, "edit")
        ]


class _OAuthUser(HamUser):

    def __init__(self, **kwargs):
        self.access_token = kwargs.get('access_token', None)
        kwargs.pop('access_token')
        super(_OAuthUser, self).__init__(**kwargs)
        self.username = self.email

    def authenticate(self, request): # pragma: no cover
        return remember(request, self.username)

    def deauthenticate(self, request): # pragma: no cover
        self.access_token = None
        return forget(request)

    def check_auth(self):
        if self.access_token is not None:
            exp_date = self.access_token['exp_date']
            now = time.time()
            return self if now < exp_date else None


@interface.implementer(IFacebookUser)
class HamFacebookUser(_OAuthUser):
    pass


@interface.implementer(IGoogleUser)
class HamGoogleUser(_OAuthUser):
    pass


@interface.implementer(IUserCollection)
class HamUserCollection(Collection):
    __name__ = "users"

    def insert(self, new_obj, check_member=False):
        if not IUser.providedBy(new_obj):
            raise TypeError("Cannot add non IUser to IUserCollection.") # pragma: no cover
        new_obj.password = get_hash(new_obj.password)
        return super(HamUserCollection, self).insert(new_obj, check_member)


@interface.implementer(IAuthedUser)
class HamAuthedUser(HamUser):
    pass
