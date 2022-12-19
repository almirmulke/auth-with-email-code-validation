from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mailtrap_client_mock():
    return MagicMock(send_email=AsyncMock())
