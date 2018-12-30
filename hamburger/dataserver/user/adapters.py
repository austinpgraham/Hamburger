from pyramid.interfaces import IRequest

from pyramid.security import Everyone
from pyramid.security import Authenticated

from zope import component
from zope import interface

from hamburger.dataserver.dataserver.interfaces import IPermissionedObject

from hamburger.dataserver.user.interfaces import IUser
from hamburger.dataserver.user.interfaces import IAuthedUser
from hamburger.dataserver.user.interfaces import IUserCollection
from hamburger.dataserver.user.interfaces import IPermissionCollection

from hamburger.dataserver.user.model import HamAuthedUser


@component.adapter(IUser, IPermissionedObject)
@interface.implementer(IPermissionCollection)
def get_permission_collection(user, context):
    acl = context.__acl__
    return list(set([x[-1] for x in acl if x[1] in (user.username, Everyone, Authenticated)]))


@component.adapter(IRequest)
@interface.implementer(IAuthedUser)
def _to_auth_user(request):
    auth_user = request.authenticated_userid
    collection = component.subscribers((request,), IUserCollection).pop()
    if auth_user in collection:
        user = collection[auth_user]
        auth_user = user.check_auth()
    else:
        return HamAuthedUser()
    interface.directlyProvides(auth_user, IAuthedUser)
    return auth_user
