from .router import Router

def route(path, methods=["GET"], middlewares=None):
    def decorator(func):
        # Detect if func is a method in a class by checking func.__qualname__.
        # Class methods have a qualname like "ClassName.method_name".
        if '.' in func.__qualname__:
            # It's a class method, so store route info on the function
            # to be registered later by the group decorator.
            if not hasattr(func, '__route_info__'):
                func.__route_info__ = []
            func.__route_info__.append((methods, path, middlewares))
        else:
            # It's a top-level function route, register immediately
            Router.get_instance().add_route(methods, path, func, middlewares=middlewares)
        return func
    return decorator

def group(prefix="", middlewares=None):
    def decorator_group(cls):
        # Begin a new group context
        Router.get_instance().start_group(prefix, middlewares or [])
        
        # Instantiate the class to access its methods
        instance = cls()
        
        # Now, find all methods in this class that have route info
        for attr_name in dir(instance):
            attr = getattr(instance, attr_name)
            if callable(attr) and hasattr(attr, '__route_info__'):
                # Register each route defined in this class with the group's prefix and middleware
                for (methods, path, mw) in attr.__route_info__:
                    Router.get_instance().add_route(methods, path, attr, middlewares=mw)

        # End the group context
        Router.get_instance().end_group()

        return cls
    return decorator_group
