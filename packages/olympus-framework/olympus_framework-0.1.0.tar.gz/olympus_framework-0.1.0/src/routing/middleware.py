import re
from .response import Response

class Middleware:
    def handle_pre(self, request):
        # Return None to continue or a Response to short-circuit the request.
        return None

    def handle_post(self, request, response):
        # Return modified response or response as is.
        return response

class HTTPSMiddleware(Middleware):
    def __init__(self, enforce=False):
        self.enforce = enforce

    def handle_pre(self, request):
        if self.enforce and request.scheme == 'http':
            # Enforce HTTPS
            https_url = request.url.replace("http://", "https://")
            return Response(status=301, headers={"Location": https_url}, body=b"")
        return None

class JSONResponseMiddleware(Middleware):
    # Ensures response is JSON if body is dict or list
    def handle_post(self, request, response):
        if isinstance(response.body, (dict, list)):
            return Response.json(response.body, status=response.status, headers=response.headers)
        return response
