import cgi
import json
from urllib.parse import parse_qs, urlparse

class Request:
    def __init__(self, method, path, headers, query_params, body, scheme, environ):
        self.method = method.upper()
        self.path = path
        self.headers = headers
        self.query_params = query_params
        self.body_raw = body
        self.scheme = scheme
        self.environ = environ
        self._json_cache = None
        self._form_cache = None
        self._files_cache = None

    @property
    def url(self):
        host = self.headers.get("Host", "localhost")
        return f"{self.scheme}://{host}{self.path}"

    @classmethod
    def from_environ(cls, environ):
        method = environ['REQUEST_METHOD']
        scheme = environ.get('wsgi.url_scheme', 'http')
        raw_uri = environ.get('RAW_URI', '')
        if not raw_uri:
            raw_uri = environ.get('REQUEST_URI', '')
        if raw_uri:
            parsed = urlparse(raw_uri)
            path = parsed.path
            query = parsed.query
        else:
            path = environ.get('PATH_INFO', '/')
            query = environ.get('QUERY_STRING', '')

        query_params = parse_qs(query)
        headers = {}
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                header_name = key[5:].replace('_', '-').title()
                headers[header_name] = value
        if 'CONTENT_TYPE' in environ:
            headers['Content-Type'] = environ['CONTENT_TYPE']
        if 'CONTENT_LENGTH' in environ:
            headers['Content-Length'] = environ['CONTENT_LENGTH']

        content_length = int(environ.get('CONTENT_LENGTH', '0') or '0')
        body = environ['wsgi.input'].read(content_length) if content_length > 0 else b''

        return cls(method, path, headers, query_params, body, scheme, environ)

    def json(self):
        if self._json_cache is not None:
            return self._json_cache
        try:
            self._json_cache = json.loads(self.body_raw.decode('utf-8'))
        except:
            self._json_cache = None
        return self._json_cache

    def form(self):
        if self._form_cache is not None:
            return self._form_cache
        if 'Content-Type' in self.headers:
            ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
            if ctype == 'multipart/form-data':
                self._form_cache = {}
                self._files_cache = {}
                form_data = cgi.FieldStorage(
                    fp=self.environ['wsgi.input'],
                    environ=self.environ,
                    keep_blank_values=True
                )
                for field in form_data.list or []:
                    if field.filename:
                        self._files_cache[field.name] = field
                    else:
                        self._form_cache[field.name] = field.value
            elif ctype == 'application/x-www-form-urlencoded':
                self._form_cache = {k: v[0] if len(v)==1 else v for k,v in parse_qs(self.body_raw.decode('utf-8')).items()}
            else:
                self._form_cache = {}
        else:
            self._form_cache = {}
        return self._form_cache

    def files(self):
        if self._files_cache is not None:
            return self._files_cache
        # Trigger form parsing if not done
        self.form()
        return self._files_cache if self._files_cache else {}

    def param(self, name, default=None):
        route_params = self.environ.get('olympus.route_params', {})
        return route_params.get(name, default)
