from hamburger.dataserver.dataserver.interfaces import IDataserver

from hamburger.dataserver.dataserver.model import Dataserver

from hamburger.dataserver.user.model import HamUserCollection


def appmaker(zodb_root):
    if 'app_root' not in zodb_root:
        app_root = Dataserver()
        zodb_root['app_root'] = app_root
        usercollection = HamUserCollection()
        app_root[usercollection.__name__] = usercollection
        import transaction
        transaction.commit()
    return zodb_root['app_root']
