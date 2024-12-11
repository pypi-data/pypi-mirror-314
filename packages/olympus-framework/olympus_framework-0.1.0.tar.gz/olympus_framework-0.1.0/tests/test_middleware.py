import unittest
from utils import wsgi_test_request

class TestMiddleware(unittest.TestCase):
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
        from src.routing.middleware import Middleware
        from src.routing.decorators import route

        class TestPreMiddleware(Middleware):
            def handle_pre(self, request):
                if request.path == "/blocked":
                    return Response(status=403, body="Forbidden")
                return None

        Router._instance = None
        cls.router = Router.get_instance()
        cls.exceptions_manager = ExceptionsManager()
        cls.router.set_exceptions_manager(cls.exceptions_manager)

        def handle_not_found(exc, request):
            return Response(status=404, body="Not Found")
        cls.exceptions_manager.register_handler(HttpNotFoundException, handle_not_found)

        cls.router.use_global_middleware(TestPreMiddleware())

        # Define a route for "allowed"
        def allowed(req):
            return {"status": "ok"}
        cls.router.add_route(["GET"], "/allowed", allowed)

    def test_blocked_route(self):
        status, headers, body = wsgi_test_request(path='/blocked')
        self.assertIn("403", status)
        self.assertIn(b"Forbidden", body)

    def test_allowed_route(self):
        status, headers, body = wsgi_test_request(path='/allowed')
        self.assertIn("200", status)
        self.assertIn(b'"status": "ok"', body)
