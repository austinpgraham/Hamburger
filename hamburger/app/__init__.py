import json

from pyramid.view import view_defaults

from pyramid.httpexceptions import HTTPOk
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import exception_response

from zope import component

from hamburger.dataserver.user.interfaces import IAuthedUser
from hamburger.dataserver.user.interfaces import IUserCollection

from hamburger.dataserver.dataserver.adapters import to_external_object

from hamburger.dataserver.dataserver.interfaces import ICollection


class AbstractView():

    def __init__(self, context, request):
        self.context = context
        self.request = request


class AbstractAuthenticatedView(AbstractView):

    def __init__(self, context, request):
        super(AbstractAuthenticatedView, self).__init__(context, request)
        found_user = IAuthedUser(request)
        self.auth_user = None if found_user.is_empty() else found_user


@view_defaults(request_method="GET",
               renderer="json",
               permission="view")
class AbstractResourceGetView(AbstractAuthenticatedView):

    def __call__(self):
        obj = to_external_object(self.context, self.request)
        return exception_response(200, body=json.dumps(obj))


@view_defaults(name="edit",
               request_method="POST",
               renderer="json",
               permission="edit")
class AbstractEditObjectView(AbstractAuthenticatedView):

    def __call__(self):
        if self.auth_user is None:
            return HTTPForbidden()
        new_obj = self.request.json
        key = getattr(self.context, self.context.__key__, None)
        result = self.context.update_from_external(new_obj, self.request)
        if result is not None:
            raise exception_response(422, body=str({'error': result}))
        if key is not None and ICollection.providedBy(self.context.__parent__):
            parent = self.context.__parent__
            parent.pop(key)
            new_key = getattr(self.context, self.context.__key__)
            parent[new_key] = self.context
        return HTTPOk()
