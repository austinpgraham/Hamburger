from authomatic.adapters import WebObAdapter

from pyramid.view import view_config

from pyramid.response import Response

from pyramid.security import forget

from pyramid.httpexceptions import HTTPOk
from pyramid.httpexceptions import HTTPCreated
from pyramid.httpexceptions import HTTPConflict
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPBadRequest

from zope import component

from hamburger.app import AbstractView
from hamburger.app import AbstractResourceGetView
from hamburger.app import AbstractAuthenticatedView

from hamburger.dataserver.dataserver.interfaces import IOAuthSettings

from hamburger.dataserver.user.interfaces import IUser
from hamburger.dataserver.user.interfaces import IUserCollection

from hamburger.dataserver.user.model import HamFacebookUser


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


@view_config(context=IUserCollection,
             name="facebook",
             request_method="GET")
class LoginUserFacebookView(AbstractView):

    def __call__(self):
        response = Response()
        oauth = component.getUtility(IOAuthSettings)
        result = oauth.login(WebObAdapter(self.request, response), 'fb')
        if result:
            if result.error:
                return HTTPForbidden()
            elif result.user:
                if not (result.user.name and result.user.id):
                    result.user.update()
                first_name, last_name = result.user.name.split()
                new_user = HamFacebookUser(facebook_id=result.user.id,
                                           first_name=first_name,
                                           last_name=last_name,
                                           email=result.user.email,
                                           password="")
                self.context.insert(new_user, check_member=True)
                response.headers = new_user.authenticate(self.request)
        return response
