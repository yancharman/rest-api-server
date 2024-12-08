from flask import jsonify

class APIError(Exception):
    status_code = 500
    message = "Internal server error"

    def __init__(self, message=None, status_code=None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error": self.message,
            "status_code": self.status_code
        }

class ValidationError(APIError):
    def __init__(self, message="Validation error", status_code=400, details=None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message, status_code)

    def to_dict(self):
        response = super().to_dict()
        response["details"] = self.details
        return response

class NotFoundError(APIError):
    def __init__(self, message="Resource not found", status_code=404):
        super().__init__(message, status_code)

class InvalidDateFormatError(APIError):
    def __init__(self, message="Invalid date format, please use yyyy-mm-dd", status_code=400):
        super().__init__(message, status_code)

class InvalidObjectIdError(APIError):
    def __init__(self, message="Invalid ObjectId format", status_code=400):
        super().__init__(message, status_code)

class DuplicationError(APIError):
    def __init__(self, message="ISBN must be unique", status_code=400):
        super().__init__(message, status_code)

class InternalServerError(APIError):
    def __init__(self, message="Internal server error", status_code=500):
        super().__init__(message, status_code)

def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def handle_404_error(error):
        return jsonify({"error": "Not Found", "status_code": 404}), 404

    @app.errorhandler(500)
    def handle_500_error(error):
        return jsonify({"error": "Internal Server Error", "status_code": 500}), 500
