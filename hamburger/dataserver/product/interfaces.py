from zope import interface

from zope.schema import Bool
from zope.schema import Text
from zope.schema import Float
from zope.schema import Datetime

from hamburger.dataserver.dataserver.interfaces import ICollection


class IProductCollection(ICollection):
    """
    A collection or product lists.
    """


class IProduct(interface.Interface):
    """
    A product mapped within the system.
    """
    hamid = Text(title="Ham assigned ID",
                 required=True)

    title = Text(title="Product Title",
                 required=True)

    brand = Text(title="Product Brand",
                 required=False,
                 default=None)

    price = Float(title="Product Price",
                  required=True)


class IUserProductWishlist(ICollection):
    """
    A user product wishilist
    """
    title = Text(title="Title of the list",
                 required=True)

    created_at = Datetime(title="Date of list creation",
                          required=True)

    is_public = Bool(title="Privacy of this list",
                     required=True)
    
    access_token = Text(title="Access token to share this wishlist",
                        required=True)


class IUserProductListCollection(ICollection):
    """
    Collection of product lists
    """
