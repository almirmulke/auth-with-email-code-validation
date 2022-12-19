import random
from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException, status

from entities.user import User
from integrations.mailtrap import MailtrapClient
from services.user import UserService


class NotAuthorizedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.")


class InvalidActivationCode(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_412_PRECONDITION_FAILED, detail="Invalid activation code."
        )


class AuthenticationService:
    def __init__(
        self,
        mailtrap_client: MailtrapClient = Depends(MailtrapClient),
        user_service: UserService = Depends(UserService),
    ):
        self.mailtrap_client = mailtrap_client
        self.user_service = user_service

    def encrypt_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def generate_activation_code(self):
        return random.randint(1000, 9999), datetime.now() + timedelta(minutes=1)

    async def send_activation_code_email(self, activation_code):
        await self.mailtrap_client.send_email(
            "Activation code", f"Your activation code is {activation_code}."
        )

    @staticmethod
    def check_user_password(user: User, password: str):
        return bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))

    async def get_user_by_basic_auth(self, email, password):
        user = await self.user_service.get_user_by_email(email)
        if not user or not self.check_user_password(user, password):
            raise NotAuthorizedException()
        return user

    @staticmethod
    def is_valid_user_activation_code(user: User, activation_code: int):
        return (
            user.activation_code == activation_code
            and user.activation_code_expires_at >= datetime.now()
        )

    async def activate_user_account(self, user: User, activation_code: int):
        if not self.is_valid_user_activation_code(user, activation_code):
            raise InvalidActivationCode()

        user.is_activated = True
        await self.user_service.update_user(user)
