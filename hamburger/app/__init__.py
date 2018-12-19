from pyramid.view import view_defaults

from pyramid.httpexceptions import HTTPForbidden

from zope import component

from hamburger.dataserver.user.interfaces import IUserCollection

from hamburger.dataserver.dataserver.adapters import to_external_object


class AbstractView():

    def __init__(self, context, request):
        self.context = context
        self.request = request


class AbstractAuthenticatedView(AbstractView):

    def __init__(self, context, request):
        super(AbstractAuthenticatedView, self).__init__(context, request)
        self.auth_user = self.request.authenticated_userid
        collection = component.subscribers((request,), IUserCollection).pop()
        if self.auth_user in collection:
            user = collection[self.auth_user]
            self.auth_user = user.check_auth()
        else:
            self.auth_user = None


@view_defaults(request_method="GET",
               renderer="json",
               permission="view")
class AbstractResourceGetView(AbstractAuthenticatedView):

    def __call__(self):
        obj = to_external_object(self.context, self.request)
        return obj
