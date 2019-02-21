import os
import time
import uuid
import shutil

from authomatic.adapters import WebObAdapter

from pyramid.view import view_config
from pyramid.view import view_defaults

from pyramid.response import Response

from pyramid.httpexceptions import HTTPOk
from pyramid.httpexceptions import HTTPCreated
from pyramid.httpexceptions import HTTPConflict
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import exception_response

from zope import component

from hamburger.app import AbstractView
from hamburger.app import AbstractEditObjectView
from hamburger.app import AbstractResourceGetView
from hamburger.app import AbstractAuthenticatedView

from hamburger.dataserver.dataserver.interfaces import IDataserver
from hamburger.dataserver.dataserver.interfaces import IOAuthSettings
from hamburger.dataserver.dataserver.interfaces import IRedundancyCheck

from hamburger.dataserver.dataserver.adapters import to_external_object

from hamburger.dataserver.dataserver.security import get_hash

from hamburger.dataserver.product.model import HamProductCollection

from hamburger.dataserver.user.interfaces import IUser
from hamburger.dataserver.user.interfaces import IUserCollection

from hamburger.dataserver.user.model import HamGoogleUser
from hamburger.dataserver.user.model import HamFacebookUser


@view_config(context=IUserCollection,
             request_method="POST")
class CreateUserView(AbstractView):

    def __call__(self):
        new_user = IUser(self.request)
        checks = component.subscribers((new_user,), IRedundancyCheck)
        if any([check.check(new_user, self.request) for check in checks]) or\
           not self.context.insert(new_user, check_member=True):
            return exception_response(409)
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
            return HTTPForbidden(headers=headers)
        return HTTPOk(headers=headers)


@view_config(context=IUser,
             name="logout",
             request_method="GET")
class LogoutUserView(AbstractAuthenticatedView):

    def __call__(self):
        if self.auth_user.username != self.context.username:
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


@view_config(context=IUser,
             name="wishlists",
             request_method="POST",
             permission="edit")
class CreateWishlistView(AbstractAuthenticatedView):

    def __call__(self):
        pc = HamProductCollection.from_json(self.request.json)
        if pc is None:
            return HTTPBadRequest()
        pc.__parent__ = self.context
        if pc.title in self.context:
            return HTTPConflict()
        self.context[pc.__name__] = pc
        return HTTPCreated()


@view_config(context=IDataserver,
             name="auth",
             request_method="GET",
             renderer="json")
class VerifyAuthView(AbstractAuthenticatedView):

    def __call__(self):
        if self.auth_user is None:
            return HTTPForbidden()
        return {"username": self.auth_user.username}


@view_config(context=IUserCollection,
             name="search",
             request_method="GET",
             renderer="json")
class SearchUserView(AbstractAuthenticatedView):

    def __call__(self):
        if "query" not in self.request.params:
            return HTTPBadRequest()
        query = self.request.params['query']
        matched_users = [to_external_object(self.context[x], self.request) for x in self.context if query.upper() in x.upper()]
        return matched_users


@view_config(context=IUser)
class EditUserView(AbstractEditObjectView):
    pass


@view_config(context=IUser,
             name="avatar",
             request_method="POST",
             permission="edit")
class UploadProfilePicView(AbstractAuthenticatedView):

    def __call__(self):
        if "file" not in self.request.POST:
            return HTTPBadRequest()
        store_path = self.request.registry.settings['profile.store']
        obj = self.request.POST["file"]
        # This will definitely need to be handled for IE, also
        # there needs to be talk of how to better store profile pictures
        # on the future NFS system.
        #
        # NOTE: Research this.
        filename = obj.filename
        _file = obj.file
        _hashed = str(get_hash(self.context.username))
        user_dir_path = os.path.join(store_path, _hashed)
        if not os.path.isdir(user_dir_path):
            os.makedirs(user_dir_path)
        full_path = os.path.join(user_dir_path, '{}.png'.format(uuid.uuid4()))
        # Write a temporary file in case of errors
        temp_path = full_path + "~"
        _file.seek(0)
        with open(temp_path, 'wb') as _out:
            shutil.copyfileobj(_file, _out)
        os.rename(temp_path, full_path)
        self.context.profile_pic = full_path
        return HTTPOk()
