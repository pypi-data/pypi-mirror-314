import unittest
import os
from utils import wsgi_test_request

class TestResponses(unittest.TestCase):
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
        from src.routing.decorators import route

        # Create a README.md file for the file route
        with open("README.md", "w") as f:
            f.write("Test file content")

        Router._instance = None
        cls.router = Router.get_instance()
        cls.exceptions_manager = ExceptionsManager()
        cls.router.set_exceptions_manager(cls.exceptions_manager)

        def handle_not_found(exc, req):
            return Response(status=404, body="Not Found")
        cls.exceptions_manager.register_handler(HttpNotFoundException, handle_not_found)

        def json_route(req):
            return {"message": "Hello JSON"}
        cls.router.add_route(["GET"], "/json", json_route)

        def html_route(req):
            return Response.html("<h1>Hello HTML</h1>")
        cls.router.add_route(["GET"], "/html", html_route)

        def file_route(req):
            return Response.file("README.md", download_name="README.txt")
        cls.router.add_route(["GET"], "/file", file_route)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("README.md"):
            os.remove("README.md")

    def test_json_response(self):
        status, headers, body = wsgi_test_request(path='/json')
        self.assertIn("200", status, f"Status: {status}, Body: {body}")
        self.assertIn(b'"message": "Hello JSON"', body)
        self.assertEqual(headers.get("Content-Type"), "application/json; charset=utf-8")

    def test_html_response(self):
        status, headers, body = wsgi_test_request(path='/html')
        self.assertIn("200", status, f"Status: {status}, Body: {body}")
        self.assertIn(b"<h1>Hello HTML</h1>", body)
        self.assertEqual(headers.get("Content-Type"), "text/html; charset=utf-8")

    def test_file_response(self):
        status, headers, body = wsgi_test_request(path='/file')
        self.assertIn("200", status, f"Status: {status}, Body: {body}")
        self.assertIn("application/octet-stream", headers.get("Content-Type",""))
        self.assertIn("README.txt", headers.get("Content-Disposition",""))
        self.assertIn(b"Test file content", body)