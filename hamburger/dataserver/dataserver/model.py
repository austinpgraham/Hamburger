from persistent.mapping import PersistentMapping

from zope import interface

from hamburger.dataserver.dataserver.interfaces import ISimonAPI
from hamburger.dataserver.dataserver.interfaces import IDataserver
from hamburger.dataserver.dataserver.interfaces import ICollection
from hamburger.dataserver.dataserver.interfaces import IContained

from hamburger.dataserver.dataserver.external import ExternalPersistentMapping
from hamburger.dataserver.dataserver.external import ExternalPersistent


@interface.implementer(IDataserver)
class Dataserver(PersistentMapping): # pragma: no cover
    __parent__ = __name__ = None


@interface.implementer(ICollection)
class Collection(ExternalPersistentMapping):

    def insert(self, new_obj, check_member=False, update_on_found=True):
        if not IContained.providedBy(new_obj): # pragma: no cover
            raise TypeError("new_obj must implement IContained.")
        key = new_obj.get_key()
        if check_member and key in self:
            if update_on_found:
                self.update(new_obj)
                return True
            return False
        new_obj.__name__ = new_obj.get_key()
        new_obj.__parent__ = self
        self[new_obj.__name__] = new_obj
        return True

    def update(self, obj):
        old_obj = self.get(obj.get_key(), None)
        if old_obj is not None:
            self[old_obj.get_key()] = obj


@interface.implementer(IContained)
class Contained(ExternalPersistent):

    __key__ = None

    def get_key(self):
        return getattr(self, self.__key__)


@interface.implementer(ISimonAPI)
class SimonAPI():
    """
    Returns the configured Simon API endpoint.
    """

    def __init__(self, endpoint):
        self.endpoint = endpoint
