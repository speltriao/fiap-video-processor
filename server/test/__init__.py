from typing import Any
from unittest.mock import patch


def mock_exception_handler_decorator(f):
    """Decorate by doing nothing.
    The exception handler should not be called in tests.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)

    return decorated_function


patch("server.exception_handler.exception_handler", mock_exception_handler_decorator).start()

import asyncio
import os
from functools import wraps

import pytest
from mockito import when


@pytest.fixture(scope="session")
async def tests_setup():
    # Mock environment variables
    when(os).getenv("AWS_ACCESS_KEY_ID").thenReturn("mock_access_key")
    when(os).getenv("AWS_SECRET_ACCESS_KEY").thenReturn("mock_secret_key")
    when(os).getenv("AWS_SESSION_TOKEN").thenReturn("mock_session_token")


future_none = asyncio.Future().set_result(None)


async def return_none():
    return None


def to_future(input_future: Any):
    future = asyncio.Future()
    future.set_result(input_future)
    return future
