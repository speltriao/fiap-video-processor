import asyncio
import os

import pytest
from mockito import mock, when


@pytest.fixture(scope="session")
async def tests_setup():
    # Mock environment variables
    when(os).getenv("AWS_ACCESS_KEY_ID").thenReturn("mock_access_key")
    when(os).getenv("AWS_SECRET_ACCESS_KEY").thenReturn("mock_secret_key")
    when(os).getenv("AWS_SESSION_TOKEN").thenReturn("mock_session_token")


future_none = asyncio.Future()
future_none.set_result(None)
