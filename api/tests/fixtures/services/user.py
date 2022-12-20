from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def user_service_mock():
    return MagicMock(
        create_user=AsyncMock(return_value=MagicMock()),
        get_user_by_email=AsyncMock(return_value=MagicMock()),
        update_user=AsyncMock(return_value=MagicMock()),
    )
