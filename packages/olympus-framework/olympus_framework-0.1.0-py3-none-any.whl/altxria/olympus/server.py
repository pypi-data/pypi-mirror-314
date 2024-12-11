from wsgiref.simple_server import make_server
from .routing.router import Router
from .routing.request import Request
from .routing.response import Response
from .exceptions_manager import ExceptionsManager
from .routing.exceptions import HttpNotFoundException, HttpMethodNotAllowedException
from .routing.middleware import HTTPSMiddleware

def application(environ, start_response):
    request = Request.from_environ(environ)
    router = Router.get_instance()

    # If global HTTPS is enforced
    if router.enforce_https_global:
        https_mw = HTTPSMiddleware(enforce=True)
        redirect_res = https_mw.handle_pre(request)
        if redirect_res:
            start_response(redirect_res.status_line, list(redirect_res.headers.items()))
            return [redirect_res.body]

    # Handle request in a try/except so that all exceptions go through ExceptionsManager
    try:
        response = router.handle_request(request)
    except Exception as e:
        if router.exceptions_manager:
            response = router.exceptions_manager.handle_exception(e, request)
        else:
            response = Response(status=500, body="Internal Server Error")

    start_response(response.status_line, list(response.headers.items()))
    return [response.body]

def run_server(host="127.0.0.1", port=8000):
    print(f"Serving on http://{host}:{port}")
    with make_server(host, port, application) as httpd:
        httpd.serve_forever()
