from datetime import datetime

import pytest


@pytest.fixture
def user_data():
    return {
        "email": "default@email.com",
        "password": "password",
        "activation_code": 1234,
        "activation_code_expires_at": datetime.now(),
        "is_activated": False,
    }
