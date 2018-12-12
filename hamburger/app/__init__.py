from pyramid.view import view_defaults

from pyramid.httpexceptions import HTTPForbidden


class AbstractView():

    def __init__(self, context, request):
        self.context = context
        self.request = request


class AbstractAuthenticatedView(AbstractView):

    def __init__(self, context, request):
        super(AbstractAuthenticatedView, self).__init__(context, request)
        self.auth_user = self.request.authenticated_userid


@view_defaults(request_method="GET",
               renderer="json")
class AbstractResourceGetView(AbstractAuthenticatedView):

    def __call__(self):
        if self.auth_user is None:
            return HTTPForbidden()
        return self.context.to_json()
