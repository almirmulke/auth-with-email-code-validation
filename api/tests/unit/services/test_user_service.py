from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from psycopg2 import IntegrityError

from services.user import UserService


class TestUserService:
    @pytest.mark.asyncio
    async def test_create_user(self, user_repository_mock):
        assert (
            await UserService(user_repository_mock).create_user(user_data_mock := MagicMock())
            == user_repository_mock.save.return_value
        )
        user_repository_mock.save.assert_called_once_with(user_data_mock)

    @pytest.mark.asyncio
    async def test_create_user_handles_db_integrity_error(self, user_repository_mock):
        user_repository_mock.save.side_effect = IntegrityError()
        with pytest.raises(HTTPException):
            await UserService(user_repository_mock).create_user(user_data_mock := MagicMock())
            user_repository_mock.save.assert_called_once_with(user_data_mock)

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, user_repository_mock):
        assert (
            await UserService(user_repository_mock).get_user_by_email(email_mock := MagicMock())
            == user_repository_mock.get_user_by_email.return_value
        )
        user_repository_mock.get_user_by_email.assert_called_once_with(email_mock)

    @pytest.mark.asyncio
    async def test_update_user(self, user_repository_mock):
        assert (
            await UserService(user_repository_mock).update_user(user_mock := MagicMock())
            == user_repository_mock.update.return_value
        )
        user_repository_mock.update.assert_called_once_with(user_mock)
