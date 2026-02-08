"""
Shared error handling module with consistent error format.
"""


class ChatBotError(Exception):
    """
    Base exception class for chatbot-related errors.
    """
    def __init__(self, message: str, error_code: str = "CHAT_ERROR", status_code: int = 500):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(ChatBotError):
    """
    Exception raised for authentication-related errors.
    """
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTH_ERROR", 401)


class AuthorizationError(ChatBotError):
    """
    Exception raised for authorization-related errors.
    """
    def __init__(self, message: str = "Authorization failed"):
        super().__init__(message, "AUTHZ_ERROR", 403)


class ValidationError(ChatBotError):
    """
    Exception raised for validation-related errors.
    """
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, "VALIDATION_ERROR", 400)


class ResourceNotFoundError(ChatBotError):
    """
    Exception raised when a requested resource is not found.
    """
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, "RESOURCE_NOT_FOUND", 404)


class DatabaseError(ChatBotError):
    """
    Exception raised for database-related errors.
    """
    def __init__(self, message: str = "Database error occurred"):
        super().__init__(message, "DATABASE_ERROR", 500)


def format_error_response(error: ChatBotError) -> dict:
    """
    Format error response in a consistent structure.

    Args:
        error: The ChatBotError exception

    Returns:
        Dictionary with consistent error structure
    """
    return {
        "error": error.message,
        "error_code": error.error_code,
        "status_code": error.status_code
    }


def handle_error(error: Exception) -> dict:
    """
    Handle generic error and return appropriate response.

    Args:
        error: The exception to handle

    Returns:
        Dictionary with error response
    """
    if isinstance(error, ChatBotError):
        return format_error_response(error)
    else:
        # For unknown errors, return a generic 500 response
        generic_error = ChatBotError(str(error))
        return format_error_response(generic_error)