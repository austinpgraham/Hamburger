from pyramid.security import Everyone
from pyramid.security import Authenticated

from zope import component
from zope import interface

from hamburger.dataserver.dataserver.interfaces import IPermissionedObject

from hamburger.dataserver.user.interfaces import IUser
from hamburger.dataserver.user.interfaces import IPermissionCollection


@component.adapter(IUser, IPermissionedObject)
@interface.implementer(IPermissionCollection)
def get_permission_collection(user, context):
    acl = context.__acl__
    return list(set([x[-1] for x in acl if x[1] in (user.username, Everyone, Authenticated)]))
