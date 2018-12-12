from persistent import Persistent

from persistent.mapping import PersistentMapping

from zope import interface

from hamburger.dataserver.dataserver.interfaces import IExternalPersistent


class AbstractExternal():

    KEYS = []
    EXCLUDE = []

    def to_json(self):
        result = {}
        for k in self.KEYS:
            if k not in self.EXCLUDE:
                result[k] = getattr(self, k)
        return result

    def is_complete(self):
        return all([getattr(self, x, None) for x in self.KEYS])

    @classmethod
    def from_json(cls, json):
        if any([key not in cls.KEYS for key in json.keys()]):
            return None
        return cls(**json)


@interface.implementer(IExternalPersistent)
class ExternalPersistent(Persistent, AbstractExternal):
    pass


@interface.implementer(IExternalPersistent)
class ExternalPersistentMapping(PersistentMapping, AbstractExternal):
    pass
