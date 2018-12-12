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


class IUserCollection(interface.Interface):
    """
    Interface representing the collection of total users.
    """

    def authenticate(user, request):
        """
        Login a give user object.
        """
