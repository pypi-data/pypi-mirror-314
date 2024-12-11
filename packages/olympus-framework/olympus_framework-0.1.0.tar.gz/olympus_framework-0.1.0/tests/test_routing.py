import unittest
from utils import wsgi_test_request

class TestRouting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import sys
        import os

        # Add the project root directory to sys.path to allow importing from `src`
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        sys.path.append(project_root)
        from src.routing.router import Router
        from src.exceptions_manager import ExceptionsManager
        from src.routing.exceptions import HttpNotFoundException
        from src.routing.response import Response

        Router._instance = None
        cls.router = Router.get_instance()
        cls.exceptions_manager = ExceptionsManager()
        cls.router.set_exceptions_manager(cls.exceptions_manager)

        # Default 404 handler
        def handle_not_found(exc, request):
            return Response(status=404, body="Not Found")
        cls.exceptions_manager.register_handler(HttpNotFoundException, handle_not_found)

        # Define a route handler and add the route programmatically
        def hello(req):
            return {"message": "Hello World"}
        cls.router.add_route(["GET"], "/hello", hello)

    def test_route_found(self):
        status, headers, body = wsgi_test_request(path='/hello')
        self.assertIn("200", status)
        self.assertIn(b'"message": "Hello World"', body)

    def test_route_not_found(self):
        status, headers, body = wsgi_test_request(path='/does-not-exist')
        self.assertIn("404", status)
        self.assertIn(b"Not Found", body)
