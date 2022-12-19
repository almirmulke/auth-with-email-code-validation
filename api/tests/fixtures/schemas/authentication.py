import pytest

from schemas.authentication import UserSignUpSchema


@pytest.fixture
def user_sign_up_schema():
    return UserSignUpSchema(
        email="default@gmail.com",
        password="defaultpass",
    )


@pytest.fixture
def user_sign_up_data():
    return {
        "email": "default@gmail.com",
        "password": "defaultpass",
    }


@pytest.fixture
def activate_account_data():
    return {"activation_code": 1234}
