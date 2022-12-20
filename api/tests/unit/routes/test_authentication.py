import pytest


class TestAuthenticationRoutes:
    @pytest.mark.asyncio
    async def test_sign_up(self, async_client, authentication_controller_mock, user_sign_up_data):
        async with async_client:
            response = await async_client.request(
                method="POST", url="auth/sign-up", json=user_sign_up_data
            )
            authentication_controller_mock.sign_up.assert_called_once()
            assert response.status_code == 201
            assert response.json() == {"email": "default@gmail.com"}

    @pytest.mark.asyncio
    async def test_activate_account(
        self,
        async_client,
        authentication_controller_mock,
        activate_account_data,
        override_auth_middlware,
        default_user,
    ):
        async with async_client:
            response = await async_client.request(
                method="PATCH", url="auth/activate-account", json=activate_account_data
            )
            authentication_controller_mock.activate_user_account.assert_called_once_with(
                default_user, activate_account_data.get("activation_code")
            )
            assert response.status_code == 200
