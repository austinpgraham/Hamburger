from pyramid_zodbconn import get_connection

from hamburger.dataserver.dataserver.interfaces import IRedundancyCheck

from hamburger.dataserver.user.interfaces import IUser
from hamburger.dataserver.user.interfaces import IUserCollection


def _get_user_collection(context):
    conn = get_connection(context)
    root = conn.root()
    return root['app_root']['users']


class AbstractUserCheck():

    def __init__(self, context):
        self.context = context

    def check(self, obj, request):
        user_collection = _get_user_collection(request)
        # If I'm checked with the context included, I'll always
        # come up redundant
        objs = [getattr(user_collection[u], self.ATTR) for u in user_collection if u != obj.username]
        return getattr(obj, self.ATTR) in objs


class CheckEmail(AbstractUserCheck):
    ATTR = "email"


class CheckUsername(AbstractUserCheck):
    ATTR = "username"
