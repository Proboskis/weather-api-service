# File: app/utils/error_handler.py

from functools import wraps
from app.utils.logger import Logger

logger = Logger.get_logger()

class ErrorHandler:
    """Error handler utility implementing the Strategy Design Pattern."""

    @staticmethod
    def handle_error(strategy):
        """Decorator for async functions."""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    strategy(e)
                    # Return a generic error response to the caller
                    return {"error": "An unexpected error occurred."}
            return wrapper
        return decorator

    @staticmethod
    def handle_error_sync(strategy):
        """Decorator for sync functions."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    strategy(e)
                    # For a critical error in sync code (like startup),
                    # fail fast after logging the error.
                    raise SystemExit(
                        "A critical error occurred during initialization; the application must shut down."
                    ) from e
            return wrapper
        return decorator

class LogErrorStrategy:
    """Default strategy to log errors."""
    @staticmethod
    def handle(exception):
        logger.error(f"Unhandled error: {exception}")
