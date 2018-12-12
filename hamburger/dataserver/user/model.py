from zope import interface

from pyramid.security import remember

from hamburger.dataserver.user.interfaces import IUser
from hamburger.dataserver.user.interfaces import IUserCollection

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
        'password'
    ]

    EXCLUDE = [
        'password'
    ]

    def __init__(self, username=None, first_name=None,
                 last_name=None, email=None,
                 password=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def authenticate(self, password, request):
        if check_hash(password, self.password):
            return remember(request, self.get_key())
        return None


@interface.implementer(IUserCollection)
class HamUserCollection(Collection):
    __name__ = "users"

    def insert(self, new_obj, check_member=False):
        if not IUser.providedBy(new_obj):
            raise TypeError("Cannot add non IUser to IUserCollection.")
        new_obj.password = get_hash(new_obj.password)
        return super(HamUserCollection, self).insert(new_obj, check_member)
