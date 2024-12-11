from .route import Route
from .response import Response
from .exceptions import HttpNotFoundException, HttpMethodNotAllowedException

class Router:
    _instance = None

    def __init__(self):
        self.routes = []
        self.group_stack = []
        self.exceptions_manager = None
        self.global_middlewares = []
        self.global_post_middlewares = []
        self.enforce_https_global = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_route(self, methods, path, handler, middlewares=None):
        prefix = ""
        group_middlewares = []
        for g in self.group_stack:
            prefix += g['prefix']
            group_middlewares.extend(g['middlewares'])
        full_path = prefix + path
        all_middlewares = (middlewares or []) + group_middlewares
        r = Route(methods, full_path, handler, middlewares=all_middlewares)
        self.routes.append(r)

    def start_group(self, prefix="", middlewares=None):
        self.group_stack.append({
            'prefix': prefix,
            'middlewares': middlewares or []
        })

    def end_group(self):
        self.group_stack.pop()

    def use_global_middleware(self, middleware):
        self.global_middlewares.append(middleware)

    def use_global_post_middleware(self, middleware):
        self.global_post_middlewares.append(middleware)

    def set_exceptions_manager(self, manager):
        self.exceptions_manager = manager

    def force_https(self, enforce=True):
        self.enforce_https_global = enforce

    def find_route(self, request):
        matched = []
        for route in self.routes:
            if route.matches(request.method, request.path):
                matched.append(route)
        return matched

    def handle_request(self, request):
        # Apply global pre middlewares
        for mw in self.global_middlewares:
            res = mw.handle_pre(request)
            if res is not None:
                return res

        # Find route
        matched_routes = self.find_route(request)
        if not matched_routes:
            # Check if any route matches the path with a different method
            all_paths = [r for r in self.routes if r.regex.match(request.path)]
            if all_paths:
                # There's at least one route with same path but different method
                from .exceptions import HttpMethodNotAllowedException
                raise HttpMethodNotAllowedException("Method not allowed")
            # No route at all matches the path -> not found
            from .exceptions import HttpNotFoundException
            raise HttpNotFoundException("Route not found")

        # For simplicity, if multiple matched (due to multiple methods?), we take the first.
        # Usually route pattern is unique for each method.
        route = matched_routes[0]
        route_params = route.extract_params(request.path)
        request.environ['olympus.route_params'] = route_params

        # Apply route-level pre middlewares
        for mw in route.middlewares:
            res = mw.handle_pre(request)
            if res is not None:
                return res

        # Call handler
        try:
            response = route.handler(request)
            if not isinstance(response, Response):
                # Handler can return dict for JSON, str for HTML, etc.
                if isinstance(response, dict) or isinstance(response, list):
                    response = Response.json(response)
                elif isinstance(response, str):
                    response = Response.html(response)
                else:
                    # Unknown type, convert to string
                    response = Response(body=str(response))
        except Exception as e:
            if self.exceptions_manager:
                response = self.exceptions_manager.handle_exception(e, request)
            else:
                # No exception manager set, return a generic 500
                response = Response(status=500, body="Internal Server Error")

        # Apply route-level post middlewares
        for mw in reversed(route.middlewares):
            response = mw.handle_post(request, response)

        # Apply global post middlewares
        for mw in reversed(self.global_post_middlewares):
            response = mw.handle_post(request, response)

        return response
  