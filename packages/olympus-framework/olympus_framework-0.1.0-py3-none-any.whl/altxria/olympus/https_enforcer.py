from .routing.response import Response

class HTTPSEnforcer:
    def __init__(self, enforce_global=False):
        self.enforce_global = enforce_global

    def enforce(self, request):
        if self.enforce_global and request.scheme != 'https':
            https_url = request.url.replace("http://", "https://")
            return Response(status=301, headers={"Location": https_url}, body=b"")
        return None
