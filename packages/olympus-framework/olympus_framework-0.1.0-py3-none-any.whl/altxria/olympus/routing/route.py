import re

class Route:
    PARAM_PATTERN = re.compile(r'<(\w+):(\w+)>')

    def __init__(self, methods, path, handler, middlewares=None):
        self.methods = [m.upper() for m in methods]
        self.path = path
        self.handler = handler
        self.middlewares = middlewares or []
        self.param_names, self.regex = self.compile_path(path)

    def compile_path(self, path):
        param_names = []
        matches = self.PARAM_PATTERN.findall(path)
        for (typ, name) in matches:
            param_names.append(name)
            if typ == 'int':
                regex_part = f"(?P<{name}>\\d+)"
            elif typ == 'str':
                regex_part = f"(?P<{name}>[^/]+)"
            else:
                # default to str if unknown
                regex_part = f"(?P<{name}>[^/]+)"
            path = path.replace(f"<{typ}:{name}>", regex_part)
        regex = re.compile(f"^{path}$")
        return param_names, regex

    def matches(self, method, path):
        if method not in self.methods:
            return False
        return self.regex.match(path) is not None

    def extract_params(self, path):
        m = self.regex.match(path)
        if not m:
            return {}
        return m.groupdict()
