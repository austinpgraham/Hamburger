from zope import component
from zope import interface

from pyramid.interfaces import IRequest

from hamburger.dataserver.dataserver.interfaces import IExternalObject
from hamburger.dataserver.dataserver.interfaces import IExternalizedObject


@interface.implementer(IExternalizedObject)
@component.adapter(IExternalObject, IRequest)
class _ExternalAdapter():
    """
    This is the base adapter for an externalization
    procedure. Simply calls the to_json on the object.
    If one is not defined and AbstractExternal is in the
    parent chain, the base to_json is used.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def to_json(self):
        # Check permissions before externalized
        if self.request.has_permission("view", context=self.context):
            return self.context.to_json(self.request)
        return None # pragma: no cover


def to_external_object(context, request):
    # Get the externalization adapter and convert to JSON
    adapter = component.queryMultiAdapter((context, request), IExternalizedObject)
    return adapter.to_json()
