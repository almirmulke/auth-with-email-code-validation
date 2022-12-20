from unittest.mock import MagicMock

import pytest

from controllers.authentication import AuthenticationController


class TestAuthenticationController:
    @pytest.mark.asyncio
    async def test_sign_up(
        self, user_service_mock, authentication_service_mock, user_sign_up_schema
    ):
        password = user_sign_up_schema.password
        assert (
            await AuthenticationController(user_service_mock, authentication_service_mock).sign_up(
                user_sign_up_schema
            )
            == user_service_mock.create_user.return_value.to_dict.return_value
        )
        authentication_service_mock.encrypt_password.assert_called_once_with(password)
        authentication_service_mock.generate_activation_code.assert_called_once()
        create_user_callargs = user_sign_up_schema.dict()
        create_user_callargs[
            "activation_code"
        ] = authentication_service_mock.generate_activation_code.return_value[0]
        create_user_callargs[
            "activation_code_expires_at"
        ] = authentication_service_mock.generate_activation_code.return_value[1]
        user_service_mock.create_user.assert_called_once_with(create_user_callargs)
        authentication_service_mock.send_activation_code_email.assert_called_once_with(
            authentication_service_mock.generate_activation_code.return_value[0]
        )

    @pytest.mark.asyncio
    async def test_activate_user_account(self, user_service_mock, authentication_service_mock):
        await AuthenticationController(
            user_service_mock, authentication_service_mock
        ).activate_user_account(user_mock := MagicMock(), activation_code_mock := MagicMock())
        authentication_service_mock.activate_user_account.assert_called_with(
            user_mock, activation_code_mock
        )
