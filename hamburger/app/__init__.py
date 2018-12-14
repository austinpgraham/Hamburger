from pyramid.view import view_defaults

from pyramid.httpexceptions import HTTPForbidden

from zope import component

from hamburger.dataserver.user.interfaces import IUserCollection


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
               renderer="json")
class AbstractResourceGetView(AbstractAuthenticatedView):

    def __call__(self):
        if self.auth_user is None:
            return HTTPForbidden()
        return self.context.to_json()
