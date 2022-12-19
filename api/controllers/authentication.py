from fastapi import Depends

from schemas.authentication import UserSignUpSchema
from services.authentication import AuthenticationService
from services.user import UserService


class AuthenticationController:
    def __init__(
        self,
        user_service: UserService = Depends(UserService),
        authentication_service: AuthenticationService = Depends(AuthenticationService),
    ):
        self.authentication_service: AuthenticationService = authentication_service
        self.user_service: UserService = user_service

    async def sign_up(self, user_data: UserSignUpSchema) -> dict:
        user_data.password = self.authentication_service.encrypt_password(user_data.password)
        user_data = user_data.dict()
        (
            user_data["activation_code"],
            user_data["activation_code_expires_at"],
        ) = self.authentication_service.generate_activation_code()  # noqa: E501
        user = await self.user_service.create_user(user_data)
        await self.authentication_service.send_activation_code_email(
            user_data.get("activation_code")
        )
        return user.to_dict()

    async def activate_user_account(self, user, activation_code):
        await self.authentication_service.activate_user_account(user, activation_code)
