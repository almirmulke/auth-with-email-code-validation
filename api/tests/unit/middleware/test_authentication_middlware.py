from unittest.mock import MagicMock

import pytest

from middlwares.authentication import authentication_middlware


class TestAuthenticationMiddleware:
    @pytest.mark.asyncio
    async def test_authentication_middleware(self, authentication_service_mock):
        await authentication_middlware(
            request_mock := MagicMock(),
            credentials_mock := MagicMock(),
            authentication_service_mock,
        )

        authentication_service_mock.get_user_by_basic_auth.assert_called_once_with(
            credentials_mock.username, credentials_mock.password
        )
        assert request_mock.user == authentication_service_mock.get_user_by_basic_auth.return_value
