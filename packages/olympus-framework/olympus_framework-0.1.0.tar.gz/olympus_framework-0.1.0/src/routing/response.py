import mimetypes
import json
import os

class Response:
    def __init__(self, status=200, headers=None, body=None):
        self.status = status
        self.headers = headers or {}
        self.body = body if body is not None else b''
        if isinstance(self.body, str):
            self.body = self.body.encode('utf-8')

    @property
    def status_line(self):
        return f"{self.status} {self.get_status_text()}"

    def get_status_text(self):
        status_map = {
            200: 'OK',
            301: 'Moved Permanently',
            302: 'Found',
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            405: 'Method Not Allowed',
            422: 'Unprocessable Entity',
            500: 'Internal Server Error'
        }
        return status_map.get(self.status, 'OK')

    @classmethod
    def json(cls, data, status=200, headers=None):
        if headers is None:
            headers = {}
        headers['Content-Type'] = 'application/json; charset=utf-8'
        return cls(status=status, headers=headers, body=json.dumps(data))

    @classmethod
    def html(cls, html_str, status=200, headers=None):
        if headers is None:
            headers = {}
        headers['Content-Type'] = 'text/html; charset=utf-8'
        return cls(status=status, headers=headers, body=html_str)

    @classmethod
    def file(cls, filepath, status=200, headers=None, download_name=None):
        if not os.path.isfile(filepath):
            return cls(status=404, body="File not found")
        if headers is None:
            headers = {}
        mime_type, _ = mimetypes.guess_type(filepath)
        if not mime_type:
            mime_type = 'application/octet-stream'
        headers['Content-Type'] = mime_type
        if download_name:
            headers['Content-Disposition'] = f'attachment; filename="{download_name}"'
        with open(filepath, 'rb') as f:
            data = f.read()
        return cls(status=status, headers=headers, body=data)
