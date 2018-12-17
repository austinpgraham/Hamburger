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
                val = getattr(self, k)
                if IExternalPersistent.providedBy(val):
                    result[k] = val.to_json()
                else:
                    result[k] = val
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

    def to_json(self):
        result = super(ExternalPersistentMapping, self).to_json()
        result['items'] = items = {}
        for key in self:
            obj = self[key]
            if IExternalPersistent.providedBy(obj):
                obj = obj.to_json()
                if obj is not None:
                    items[key] = obj
        return result
