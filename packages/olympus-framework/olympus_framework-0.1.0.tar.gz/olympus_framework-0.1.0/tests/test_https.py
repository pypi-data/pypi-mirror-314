import unittest
from utils import wsgi_test_request

class TestHTTPS(unittest.TestCase):
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
        from src.routing.middleware import HTTPSMiddleware
        from src.routing.decorators import route

        Router._instance = None
        cls.router = Router.get_instance()
        cls.exceptions_manager = ExceptionsManager()
        cls.router.set_exceptions_manager(cls.exceptions_manager)

        def handle_not_found(exc, req):
            return Response(status=404, body="Not Found")
        cls.exceptions_manager.register_handler(HttpNotFoundException, handle_not_found)

        def secure_route(req):
            return {"secure": True}
        cls.router.add_route(["GET"], "/secure", secure_route, middlewares=[HTTPSMiddleware(enforce=True)])

    def test_https_redirect(self):
        # Should return 301 redirect to HTTPS
        status, headers, body = wsgi_test_request(path='/secure')
        self.assertIn("301", status)
        self.assertIn("Location", headers)
        self.assertTrue(headers["Location"].startswith("https://"))
