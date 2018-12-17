from hamburger.dataserver.dataserver.interfaces import IDataserver

from hamburger.dataserver.dataserver.model import Dataserver

from hamburger.dataserver.user.model import HamUserCollection

from hamburger.dataserver.product.model import HamProductCollection


def appmaker(zodb_root):
    if 'app_root' not in zodb_root:
        app_root = Dataserver()
        zodb_root['app_root'] = app_root
        usercollection = HamUserCollection()
        app_root[usercollection.__name__] = usercollection
        productcollection = HamProductCollection(title="allproducts",
                                                  is_public=True)
        app_root[productcollection.__name__] = productcollection
        import transaction
        transaction.commit()
    return zodb_root['app_root']
