from pyramid.view import view_config

from pyramid.response import Response

from pyramid.security import forget

from pyramid.httpexceptions import HTTPOk
from pyramid.httpexceptions import HTTPCreated
from pyramid.httpexceptions import HTTPConflict
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPBadRequest

from hamburger.app import AbstractView
from hamburger.app import AbstractResourceGetView
from hamburger.app import AbstractAuthenticatedView

from hamburger.dataserver.user.interfaces import IUser
from hamburger.dataserver.user.interfaces import IUserCollection


@view_config(context=IUserCollection,
             request_method="POST")
class CreateUserView(AbstractView):

    def __call__(self):
        new_user = IUser(self.request)
        if not new_user.is_complete():
            return HTTPBadRequest()
        if not self.context.insert(new_user, check_member=True):
            return HTTPConflict()
        return HTTPCreated()


@view_config(context=IUser,
             request_method='GET')
class GetUserView(AbstractResourceGetView):
    pass


@view_config(context=IUser,
             name="login",
             request_method="POST")
class LoginUserView(AbstractView):

    def __call__(self):
        if 'password' not in self.request.json:
            return HTTPBadRequest()
        password = self.request.json['password']
        headers = self.context.authenticate(password, self.request)
        if headers is None:
            return HTTPForbidden()
        return HTTPOk(headers=headers)


@view_config(context=IUser,
             name="logout",
             request_method="GET")
class LogoutUserView(AbstractAuthenticatedView):

    def __call__(self):
        super(LogoutUserView, self).__call__()
        if self.auth_user != self.context.username:
            return HTTPForbidden()
        headers = forget(self.request)
        return HTTPOk(headers=headers)
