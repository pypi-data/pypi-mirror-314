import unittest
from utils import wsgi_test_request

class TestExceptions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import sys
        import os

        # Add the project root directory to sys.path to allow importing from `src`
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        sys.path.append(project_root)
        from src.routing.router import Router
        from src.exceptions_manager import ExceptionsManager
        from src.routing.exceptions import HttpNotFoundException, BadRequestException
        from src.routing.response import Response
        from src.routing.decorators import route

        Router._instance = None
        cls.router = Router.get_instance()
        cls.exceptions_manager = ExceptionsManager()
        cls.router.set_exceptions_manager(cls.exceptions_manager)

        def handle_not_found(exc, req):
            return Response(status=404, body="Custom Not Found")
        cls.exceptions_manager.register_handler(HttpNotFoundException, handle_not_found)

        # Routes
        def bad_request_route(req):
            raise BadRequestException("Invalid input")
        cls.router.add_route(["GET"], "/raise-bad-request", bad_request_route)

        def custom_route(req):
            from src.routing.exceptions import HttpNotFoundException
            raise HttpNotFoundException("Not here")
        cls.router.add_route(["GET"], "/raise-custom", custom_route)

    def test_bad_request_no_custom_handler(self):
        # Should default to 400
        status, headers, body = wsgi_test_request(path='/raise-bad-request')
        self.assertIn("400", status)
        self.assertIn(b"Bad Request", body)

    def test_custom_not_found_handler(self):
        status, headers, body = wsgi_test_request(path='/raise-custom')
        self.assertIn("404", status)
        self.assertIn(b"Custom Not Found", body)
