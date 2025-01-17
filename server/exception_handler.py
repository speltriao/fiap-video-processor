from typing import Any, Callable

from server import env, logger
from server.adapters import SQSOutHandler


class CustomException(Exception):
    def __init__(self, id: int, message="An error occurred"):
        self.id = id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Error ID: {self.id}, Message: {self.message}"


def exception_handler(func: Callable) -> Callable:
    """Decorator to handle exceptions and log errors."""

    async def wrapper(*args: Any, **kwargs: Any) -> Callable:
        try:
            return await func(*args, **kwargs)
        except CustomException as ce:
            id_request: int = ce.id
            logger.error(f"Unhandled exception occurred: {ce.message}")
            if id_request:
                try:
                    await SQSOutHandler(env.Environment()).send_error_message(id_request)
                except Exception as send_error:
                    logger.error(f"Error sending error message: {send_error}")
            else:
                logger.error("id_request is not set, cannot send error message.")
        except Exception as e:
            logger.error(f"Unknown exception: {e}")

    return wrapper
