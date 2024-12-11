import unittest
from utils import wsgi_test_request

class TestCORS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import sys
        import os

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        sys.path.append(project_root)

        from src.routing.router import Router
        from src.exceptions_manager import ExceptionsManager
        from src.routing.exceptions import HttpNotFoundException
        from src.routing.response import Response
        from src.routing.cors import CORSMiddleware

        Router._instance = None
        cls.router = Router.get_instance()
        cls.exceptions_manager = ExceptionsManager()
        cls.router.set_exceptions_manager(cls.exceptions_manager)

        def handle_not_found(exc, req):
            return Response(status=404, body="Not Found")
        cls.exceptions_manager.register_handler(HttpNotFoundException, handle_not_found)

        # Instantiate one CORS middleware and add it as both pre and post middleware
        cors = CORSMiddleware()
        cls.router.use_global_middleware(cors)         # For pre (handle_pre)
        cls.router.use_global_post_middleware(cors)    # For post (handle_post)

        def cors_route(req):
            return {"cors": "ok"}
        cls.router.add_route(["GET"], "/cors", cors_route)

    def test_cors_headers(self):
        status, headers, body = wsgi_test_request(path='/cors')
        self.assertIn("200", status, f"Status: {status}, Body: {body}")
        self.assertEqual(headers.get("Access-Control-Allow-Origin"), "*")
        self.assertEqual(headers.get("Access-Control-Allow-Methods"), "*")
