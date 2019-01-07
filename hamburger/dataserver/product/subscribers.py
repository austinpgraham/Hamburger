from pyramid_zodbconn import get_connection


def _get_product_collection(context):
    conn = get_connection(context)
    root = conn.root()
    return root['app_root']['products']


class CheckTitle():
    ATTR = "title"

    def __init__(self, context):
        self.context = context

    def check(self, obj, request):
        collection = self.context.__parent__
        return getattr(obj, self.ATTR) in collection
