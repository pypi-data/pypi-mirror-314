from .routing.response import Response
from .routing.exceptions import (
    HttpNotFoundException, 
    HttpMethodNotAllowedException, 
    ValidationException, 
    BadRequestException
)

class ExceptionsManager:
    def __init__(self):
        self.handlers = {}  # {ExceptionClass: handler_function}

        # Default responses for known HTTP exceptions if no handler is found
        self.default_responses = {
            HttpNotFoundException: (404, "Not Found"),
            HttpMethodNotAllowedException: (405, "Method Not Allowed"),
            ValidationException: (422, "Unprocessable Entity"),
            BadRequestException: (400, "Bad Request")
        }

    def register_handler(self, exception_class, handler):
        self.handlers[exception_class] = handler

    def handle_exception(self, exception, request):
        # First, check for a custom handler
        for exc_type, handler in self.handlers.items():
            if isinstance(exception, exc_type):
                return handler(exception, request)

        # If no custom handler, check default responses
        for exc_type, (status, message) in self.default_responses.items():
            if isinstance(exception, exc_type):
                return Response(status=status, body=message)

        # If we have no mapping or handler, fallback to 500
        return Response(status=500, body="Internal Server Error")
