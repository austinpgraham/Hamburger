from zope import interface

from zope.schema import Text


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


class IUserCollection(interface.Interface):
    """
    Interface representing the collection of total users.
    """


class IFacebookUser(IUser):
    """
    Interface representing a user logged in with Facebook
    """

    facebook_id = Text(title="User Facebook ID",
                       required=True)

    access_token = Text(title="User Facebook Access Token",
                        required=True)
