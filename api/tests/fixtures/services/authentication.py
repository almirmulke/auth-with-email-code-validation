from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def authentication_service_mock():
    return MagicMock(
        encrypt_password=MagicMock(),
        generate_activation_code=MagicMock(return_value=(1234, datetime.now())),
        send_activation_code_email=AsyncMock(),
        check_user_password=MagicMock(),
        get_user_by_basic_auth=AsyncMock(),
        is_valid_user_activation_code=MagicMock(),
        activate_user_account=AsyncMock(),
    )
