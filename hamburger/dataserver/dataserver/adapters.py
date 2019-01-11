from zope import component
from zope import interface

from pyramid.interfaces import IRequest

from hamburger.dataserver.dataserver.interfaces import IExternalObject
from hamburger.dataserver.dataserver.interfaces import IExternalizedObject


@interface.implementer(IExternalizedObject)
@component.adapter(IExternalObject, IRequest)
class _ExternalAdapter():

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def to_json(self):
        if self.request.has_permission("view", context=self.context):
            return self.context.to_json(self.request)
        return None # pragma: no cover


def to_external_object(context, request):
    adapter = component.queryMultiAdapter((context, request), IExternalizedObject)
    return adapter.to_json()
