from datetime import datetime
from glob import glob
from unittest.mock import MagicMock

import pytest
from fastapi import Request
from httpx import AsyncClient

from app import app
from entities.user import User
from middlwares.authentication import authentication_middlware
from utils.database import get_db_connection

pytest_plugins = [
    fixture.replace("/", ".").replace("\\", ".").replace(".py", "")
    for fixture in glob("tests/fixtures/**/*.py", recursive=True)
    + glob("tests/integration/fixtures/**/*.py", recursive=True)
    if "__" not in fixture
]
app.dependency_overrides[get_db_connection] = lambda: MagicMock()
default_user_instance = User(
    id=1,
    email="default@email.com",
    password="defaultpass",
    activation_code=1234,
    activation_code_expires_at=datetime.now(),
    is_activated=False,
)


@pytest.fixture
def async_client():
    return AsyncClient(app=app, base_url="http://localhost")


@pytest.fixture
def default_user():
    return default_user_instance


def authentication_middlware_override(request=Request):
    request.user = default_user_instance


@pytest.fixture
def override_auth_middlware():
    app.dependency_overrides[authentication_middlware] = authentication_middlware_override
    yield
    del app.dependency_overrides[authentication_middlware]
