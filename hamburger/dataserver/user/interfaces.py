from zope import interface

from zope.schema import Dict
from zope.schema import List
from zope.schema import Text
from zope.schema import Object

from hamburger.dataserver.dataserver.interfaces import IExternalObject


class IUser(interface.Interface):
    """
    Interface representing a user in the
    Hamburger system.
    """
    username = Text(title='User login name',
                    required=True)
    first_name = Text(title='User First Name',
                      required=True)
    last_name = Text(title='User Last Name',
                     required=True)
    email = Text(title="User email",
                 required=True)
    password = Text(title="User password",
                    required=True)

    def authenticate(user, request):
        """
        Login a give user object.
        """

    def deauthenticate(request):
        """
        Logout a user
        """

    def check_auth():
        """
        Check user authentication still valid.
        """


class IUserCollection(interface.Interface):
    """
    Interface representing the collection of total users.
    """


class IOAuthUser(IUser):
    """
    OAuth provided user client.
    """
    access_token = Dict(title="User Facebook Access Token",
                        required=True)


class IAuthedUser(IUser):
    """
    A user that has been authenitcated and fetched
    via request.
    """


class IFacebookUser(IOAuthUser):
    """
    Interface representing a user logged in with Facebook
    """


class IGoogleUser(IOAuthUser):
    """
    Interface representing a user logged in with Google
    """


class IPermissionCollection(IExternalObject):
    """
    A collection of allowed permissions a user
    has on a particular object.
    """
