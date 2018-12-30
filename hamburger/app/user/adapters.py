from pyramid.interfaces import IRequest

from zope import component
from zope import interface

from hamburger.dataserver.user.interfaces import IUser

from hamburger.dataserver.user.model import HamUser


def _from_request(user_class, request):
    user = user_class()
    for k in user_class.KEYS:
        item = request.json.get(k, None)
        setattr(user, k, item)
    return user


@component.adapter(IRequest)
@interface.implementer(IUser)
def _get_user_from_request(request):
    return _from_request(HamUser, request)
