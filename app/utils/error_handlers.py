from marshmallow import ValidationError
from .helpers import error_response


def error_handlers(app):
    """Register error handlers for the Flask application"""

    @app.errorhandler(400)
    def bad_request(error):
        return error_response(
            message=getattr(error, "description", "The request was malformed or invalid"),
            status_code=400,
            error_code="BAD_REQUEST"
        )

    @app.errorhandler(401)
    def unauthorized(error):
        return error_response(
            message=getattr(error, "description", "Authentication is required to access this resource"),
            status_code=401,
            error_code="UNAUTHORIZED"
        )

    @app.errorhandler(403)
    def forbidden(error):
        return error_response(
            message=getattr(error, "description", "You do not have permission to access this resource"),
            status_code=403,
            error_code="FORBIDDEN"
        )

    @app.errorhandler(404)
    def not_found(error):
        return error_response(
            message=getattr(error, "description", "The requested resource was not found"),
            status_code=404,
            error_code="NOT_FOUND"
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return error_response(
            message=getattr(error, "description", "The HTTP method is not allowed for this endpoint"),
            status_code=405,
            error_code="METHOD_NOT_ALLOWED"
        )

    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return error_response(
            message=getattr(error, "description", "Too many requests. Please try again later."),
            status_code=429,
            error_code="RATE_LIMIT"
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return error_response(
            message=getattr(error, "description", "An unexpected error occurred on the server"),
            status_code=500,
            error_code="INTERNAL_ERROR"
        )
