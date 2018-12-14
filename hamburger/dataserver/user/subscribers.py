from pyramid_zodbconn import get_connection


def _get_user_collection(context):
    conn = get_connection(context)
    root = conn.root()
    return root['app_root']['users']
