import psycopg2
from fastapi import Depends, HTTPException, status

from entities.user import User
from repositories.user import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self.user_repository: UserRepository = user_repository

    async def create_user(self, user_data):
        try:
            return await self.user_repository.save(user_data)
        except psycopg2.IntegrityError:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                detail=f"User with email {user_data.get('email')} already exists!",
            )

    async def get_user_by_email(self, email):
        return await self.user_repository.get_user_by_email(email)

    async def update_user(self, user: User):
        return await self.user_repository.update(user)
