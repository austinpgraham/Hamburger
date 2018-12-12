from pyramid.interfaces import IRequest

from zope import component
from zope import interface

from hamburger.dataserver.user.interfaces import IUser

from hamburger.dataserver.user.model import HamUser


@component.adapter(IRequest)
@interface.implementer(IUser)
def _get_user_from_request(request):
    user = HamUser()
    for k in HamUser.KEYS:
        item = request.json.get(k, None)
        setattr(user, k, item)
    return user
