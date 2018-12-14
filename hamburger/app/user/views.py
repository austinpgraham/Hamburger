import time

from authomatic.adapters import WebObAdapter

from pyramid.view import view_config
from pyramid.view import view_defaults

from pyramid.response import Response

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

from hamburger.dataserver.user.model import HamGoogleUser
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
        headers = self.context.authenticate(self.request)
        if headers is None:
            return HTTPForbidden()
        return HTTPOk(headers=headers)


@view_config(context=IUser,
             name="logout",
             request_method="GET")
class LogoutUserView(AbstractAuthenticatedView):

    def __call__(self):
        if self.auth_user is None or self.auth_user.username != self.context.username:
            return HTTPForbidden()
        headers = self.context.deauthenticate(self.request)
        return HTTPOk(headers=headers)


@view_defaults(context=IUserCollection,
               request_method='GET')
class OAuthUserLoginView(AbstractView):
    __provider__ = None
    __user_class__ = None

    def _stamp_time(self, data):
        now = time.time()
        exp_date = float(data['expires_in']) + now
        data['exp_date'] = exp_date

    def __call__(self):
        response = Response()
        oauth = component.getUtility(IOAuthSettings)
        result = oauth.login(WebObAdapter(self.request, response), self.__provider__)
        if result:
            if result.error:
                return HTTPForbidden()
            elif result.user:
                if not (result.user.name and result.user.id):
                    result.user.update()
                self._stamp_time(result.provider.access_token_response.data)
                new_user = self.__user_class__(first_name=result.user.first_name,
                                               last_name=result.user.last_name,
                                               email=result.user.email,
                                               password="",
                                               access_token=result.provider.access_token_response.data)
                self.context.insert(new_user, check_member=True)
                response.headers = new_user.authenticate(self.request)
        return response


@view_config(name="facebook")
class LoginUserFacebookView(OAuthUserLoginView):
    __provider__ = "fb"
    __user_class__ = HamFacebookUser


@view_config(name="google")
class LoginUserGoogleView(OAuthUserLoginView):
    __provider__ = "google"
    __user_class__ = HamGoogleUser
