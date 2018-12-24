def add_cors_to_response(event):
    request = event.request
    response = event.response
    if 'Origin' in request.headers:
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,OPTIONS'


class CorsPreflightPredicate():
    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'cors_preflight = %s' % bool(self.val)
    
    phash = text

    def __call__(self, context, request):
        if not self.val:
            return False
        return (
            request.method == 'OPTIONS' and
            'HTTP_ORIGIN' in request.headers.environ and
            'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.headers.environ
        )
