import unittest
from utils import wsgi_test_request

class TestGroups(unittest.TestCase):
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
        from src.routing.decorators import route, group

        Router._instance = None
        cls.router = Router.get_instance()
        cls.exceptions_manager = ExceptionsManager()
        cls.router.set_exceptions_manager(cls.exceptions_manager)

        def handle_not_found(exc, req):
            return Response(status=404, body="Not Found")
        cls.exceptions_manager.register_handler(HttpNotFoundException, handle_not_found)

        # Manually simulate groups without decorators:
        # Start API group
        cls.router.start_group(prefix="/api", middlewares=[])
        def api_items(req):
            return {"items": ["A","B"]}
        cls.router.add_route(["GET"], "/items", api_items)
        cls.router.end_group()

        # Start admin group
        cls.router.start_group(prefix="/admin", middlewares=[])
        def admin_dashboard(req):
            return {"admin": "ok"}
        cls.router.add_route(["GET"], "/dashboard", admin_dashboard)
        cls.router.end_group()

    def test_api_group_route(self):
        status, headers, body = wsgi_test_request(path='/api/items')
        self.assertIn("200", status, f"Status: {status}, Body: {body}")
        self.assertIn(b'"items": ["A", "B"]', body)

    def test_admin_group_route(self):
        status, headers, body = wsgi_test_request(path='/admin/dashboard')
        self.assertIn("200", status, f"Status: {status}, Body: {body}")
        self.assertIn(b'"admin": "ok"', body)
