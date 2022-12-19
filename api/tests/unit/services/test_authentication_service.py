from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from services.authentication import (
    AuthenticationService,
    InvalidActivationCode,
    NotAuthorizedException,
)


class TestAuthenticationService:
    @patch("services.authentication.bcrypt")
    def test_encrypt_password(self, bcrypt_mock):
        return_value = AuthenticationService(MagicMock(), MagicMock()).encrypt_password(
            password_mock := MagicMock()
        )
        password_mock.encode.assert_called_once_with("utf-8")
        bcrypt_mock.gensalt.assert_called_once()
        bcrypt_mock.hashpw.return_value.decode.assert_called_once_with("utf-8")
        bcrypt_mock.hashpw.assert_called_once_with(
            password_mock.encode.return_value, bcrypt_mock.gensalt.return_value
        )
        assert return_value == bcrypt_mock.hashpw.return_value.decode.return_value

    @patch("services.authentication.timedelta")
    @patch("services.authentication.datetime")
    @patch("services.authentication.random")
    def test_generate_activation_code(self, random_mock, datetime_mock, timedelta_mock):
        return_value = AuthenticationService(MagicMock(), MagicMock()).generate_activation_code()
        random_mock.randint.assert_called_once_with(1000, 9999)
        datetime_mock.now.assert_called_once()
        timedelta_mock.assert_called_once_with(minutes=1)
        assert return_value == (
            random_mock.randint.return_value,
            datetime_mock.now.return_value + timedelta_mock.return_value,
        )

    @pytest.mark.asyncio
    async def test_send_activation_code_email(self, mailtrap_client_mock):
        await AuthenticationService(mailtrap_client_mock, MagicMock()).send_activation_code_email(
            activation_code_mock := MagicMock()
        )
        mailtrap_client_mock.send_email.assert_called_with(
            "Activation code", f"Your activation code is {activation_code_mock}."
        )

    @patch("services.authentication.bcrypt")
    def test_check_user_password(self, bcrypt_mock):
        assert (
            AuthenticationService(MagicMock(), MagicMock()).check_user_password(
                user_mock := MagicMock(), password_mock := MagicMock()
            )
            == bcrypt_mock.checkpw.return_value
        )
        password_mock.encode.assert_called_once_with("utf-8")
        user_mock.password.encode.assert_called_once_with("utf-8")
        bcrypt_mock.checkpw.assert_called_with(
            password_mock.encode.return_value, user_mock.password.encode.return_value
        )

    @pytest.mark.asyncio
    @patch("services.authentication.AuthenticationService.check_user_password")
    async def test_get_user_by_basic_auth(self, check_user_password_mock, user_service_mock):
        check_user_password_mock.return_value = True
        assert (
            await AuthenticationService(MagicMock(), user_service_mock).get_user_by_basic_auth(
                email_mock := MagicMock(), password_mock := MagicMock()
            )
            == user_service_mock.get_user_by_email.return_value
        )
        user_service_mock.get_user_by_email.assert_called_with(email_mock)
        check_user_password_mock.assert_called_with(
            user_service_mock.get_user_by_email.return_value, password_mock
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_mock, is_password_valid", [(None, True), (MagicMock(), False)])
    @patch("services.authentication.AuthenticationService.check_user_password")
    async def test_get_user_by_basic_auth_invalid_credentials(
        self, check_user_password_mock, user_service_mock, user_mock, is_password_valid
    ):
        check_user_password_mock.return_value = is_password_valid
        user_service_mock.get_user_by_email.return_value = user_mock
        with pytest.raises(NotAuthorizedException):
            assert (
                await AuthenticationService(MagicMock(), user_service_mock).get_user_by_basic_auth(
                    email_mock := MagicMock(), password_mock := MagicMock()
                )
                == user_service_mock.get_user_by_email.return_value
            )
            user_service_mock.get_user_by_email.assert_called_with(email_mock)
            if user_mock is not None:
                check_user_password_mock.assert_called_with(
                    user_service_mock.get_user_by_email.return_value, password_mock
                )

    @pytest.mark.parametrize(
        "user_mock, activation_code, current_time, expected_result",
        [
            (
                MagicMock(activation_code=1234, activation_code_expires_at=datetime.now()),
                1234,
                datetime.now() - timedelta(minutes=1),
                True,
            ),
            (MagicMock(activation_code=1234), 4321, None, False),
            (
                MagicMock(activation_code=1234, activation_code_expires_at=datetime.now()),
                1234,
                datetime.now() + timedelta(minutes=1),
                False,
            ),
        ],
    )
    @patch("services.authentication.datetime")
    def test_is_valid_user_activation_code(
        self, datetime_mock, user_mock, activation_code, current_time, expected_result
    ):
        datetime_mock.now.return_value = current_time
        assert (
            AuthenticationService(None, None).is_valid_user_activation_code(
                user_mock, activation_code
            )
            == expected_result
        )

    @pytest.mark.asyncio
    @patch("services.authentication.AuthenticationService.is_valid_user_activation_code")
    async def test_activate_user_account(
        self, is_valid_user_activation_code_mock, user_service_mock
    ):
        is_valid_user_activation_code_mock.return_value = True
        await AuthenticationService(None, user_service_mock).activate_user_account(
            user_mock := MagicMock(is_activated=False), activation_code=MagicMock()
        )
        assert user_mock.is_activated is True
        user_service_mock.update_user.assert_called_once_with(user_mock)

    @pytest.mark.asyncio
    @patch("services.authentication.AuthenticationService.is_valid_user_activation_code")
    async def test_activate_user_account_invalid_account_code(
        self, is_valid_user_activation_code_mock, user_service_mock
    ):
        is_valid_user_activation_code_mock.return_value = False
        with pytest.raises(InvalidActivationCode):
            await AuthenticationService(None, user_service_mock).activate_user_account(
                user_mock := MagicMock(is_activated=False), activation_code=MagicMock()
            )
            assert user_mock.is_activated is False
            user_service_mock.update_user.assert_not_called()
