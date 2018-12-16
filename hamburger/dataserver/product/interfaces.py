from zope import interface

from zope.schema import Text
from zope.schema import Float

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
