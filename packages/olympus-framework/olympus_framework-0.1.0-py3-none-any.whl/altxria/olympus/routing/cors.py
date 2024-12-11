from .middleware import Middleware

class CORSMiddleware(Middleware):
    def __init__(self, allow_origins="*", allow_methods="*", allow_headers="*", allow_credentials=False):
        self.allow_origins = allow_origins
        self.allow_methods = allow_methods
        self.allow_headers = allow_headers
        self.allow_credentials = allow_credentials

    def handle_pre(self, request):
        # Handle preflight requests if OPTIONS
        if request.method == "OPTIONS":
            from .response import Response
            headers = {
                "Access-Control-Allow-Origin": self.allow_origins,
                "Access-Control-Allow-Methods": self.allow_methods,
                "Access-Control-Allow-Headers": self.allow_headers
            }
            if self.allow_credentials:
                headers["Access-Control-Allow-Credentials"] = "true"
            return Response(status=200, headers=headers, body=b"")
        return None

    def handle_post(self, request, response):
        response.headers["Access-Control-Allow-Origin"] = self.allow_origins
        response.headers["Access-Control-Allow-Methods"] = self.allow_methods
        response.headers["Access-Control-Allow-Headers"] = self.allow_headers
        if self.allow_credentials:
            response.headers["Access-Control-Allow-Credentials"] = "true"
        return response  
