from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def user_repository_mock():
    return MagicMock(
        save=AsyncMock(return_value=MagicMock()),
        get_user_by_email=AsyncMock(return_value=MagicMock()),
        update=AsyncMock(return_value=MagicMock()),
    )
