from unittest.mock import MagicMock

import pytest
from psycopg2 import DatabaseError

from repositories.user import UserRepository


class TestUserRepository:

    # async def save(self, user_data):
    #     sql = """
    #         INSERT INTO "user"(email, password, activation_code, activation_code_expires_at)
    #         VALUES(%s, %s, %s, %s)
    #         RETURNING id, email, password, activation_code, activation_code_expires_at;
    #     """
    #     cursor = db_conn.cursor()
    #     try:
    #         cursor.execute(
    #             sql,
    #             (
    #                 user_data["email"],
    #                 user_data["password"],
    #                 user_data["activation_code"],
    #                 user_data["activation_code_expires_at"],
    #             )
    #         )
    #     except psycopg2.DatabaseError as e:
    #         cursor.close()
    #         db_conn.rollback()
    #         raise e

    #     id, email, password, activation_code, activation_code_expires_at = cursor.fetchone()
    #     db_conn.commit()
    #     cursor.close()
    #     return User(id, email, password, activation_code, activation_code_expires_at)

    @pytest.mark.asyncio
    async def test_save(self, user_data):
        sql = """
            INSERT INTO "user"(email, password, activation_code, activation_code_expires_at)
            VALUES(%s, %s, %s, %s)
            RETURNING id, email, password, activation_code, activation_code_expires_at;
        """
        db_conn_mock = MagicMock()
        db_conn_mock.cursor.return_value.fetchone.return_value = (
            1,
            user_data["email"],
            user_data["password"],
            user_data["activation_code"],
            user_data["activation_code_expires_at"],
        )
        user = await UserRepository(db_conn_mock).save(user_data)
        db_conn_mock.cursor.assert_called_once()
        db_conn_mock.cursor.return_value.execute.assert_called_with(
            sql,
            (
                user_data["email"],
                user_data["password"],
                user_data["activation_code"],
                user_data["activation_code_expires_at"],
            ),
        )
        db_conn_mock.cursor.return_value.fetchone.assert_called_once()
        db_conn_mock.commit.asser_called_once()
        db_conn_mock.cursor.return_value.close.assert_called_once()
        assert user.id == 1
        assert user.email == user_data["email"]
        assert user.password == user_data["password"]
        assert user.activation_code == user_data["activation_code"]
        assert user.activation_code_expires_at == user_data["activation_code_expires_at"]
        assert user.is_activated is False

    @pytest.mark.asyncio
    async def test_save_handles_db_error(self, user_data):
        sql = """
            INSERT INTO "user"(email, password, activation_code, activation_code_expires_at)
            VALUES(%s, %s, %s, %s)
            RETURNING id, email, password, activation_code, activation_code_expires_at;
        """
        db_conn_mock = MagicMock()
        db_conn_mock.cursor.return_value.execute.sife_effect = DatabaseError()
        db_conn_mock.cursor.return_value.fetchone.return_value = (
            1,
            user_data["email"],
            user_data["password"],
            user_data["activation_code"],
            user_data["activation_code_expires_at"],
        )
        await UserRepository(db_conn_mock).save(user_data)
        db_conn_mock.cursor.assert_called_once()
        db_conn_mock.cursor.return_value.execute.assert_called_with(
            sql,
            (
                user_data["email"],
                user_data["password"],
                user_data["activation_code"],
                user_data["activation_code_expires_at"],
            ),
        )
        db_conn_mock.cursor.return_value.close.assert_called_once()
        db_conn_mock.rollback.asser_called_once()

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, user_data):
        sql = """
            SELECT id, email, password, activation_code, activation_code_expires_at, is_activated
            FROM "user" WHERE email=%s
        """
        db_conn_mock = MagicMock()
        db_conn_mock.cursor.return_value.fetchone.return_value = (
            1,
            user_data["email"],
            user_data["password"],
            user_data["activation_code"],
            user_data["activation_code_expires_at"],
            False,
        )
        user = await UserRepository(db_conn_mock).get_user_by_email(email_mock := MagicMock())
        db_conn_mock.cursor.assert_called_once()
        db_conn_mock.cursor.return_value.execute.assert_called_once_with(sql, (email_mock,))
        db_conn_mock.cursor.return_value.fetchone.assert_called_once()
        db_conn_mock.commit.asser_called_once()
        db_conn_mock.cursor.return_value.close.assert_called_once()
        assert user.id == 1
        assert user.email == user_data["email"]
        assert user.password == user_data["password"]
        assert user.activation_code == user_data["activation_code"]
        assert user.activation_code_expires_at == user_data["activation_code_expires_at"]
        assert user.is_activated is False

    @pytest.mark.asyncio
    async def test_get_user_by_email_no_user_found(self):
        sql = """
            SELECT id, email, password, activation_code, activation_code_expires_at, is_activated
            FROM "user" WHERE email=%s
        """
        db_conn_mock = MagicMock()
        db_conn_mock.cursor.return_value.fetchone.return_value = None
        user = await UserRepository(db_conn_mock).get_user_by_email(email_mock := MagicMock())
        db_conn_mock.cursor.assert_called_once()
        db_conn_mock.cursor.return_value.execute.assert_called_once_with(sql, (email_mock,))
        db_conn_mock.cursor.return_value.close.assert_called_once()
        db_conn_mock.cursor.return_value.fetchone.assert_called_once()
        db_conn_mock.commit.asser_called_once()
        assert user is None

    @pytest.mark.asyncio
    async def test_get_user_by_email_handles_db_errors(self):
        sql = """
            SELECT id, email, password, activation_code, activation_code_expires_at, is_activated
            FROM "user" WHERE email=%s
        """
        db_conn_mock = MagicMock()
        db_conn_mock.cursor.return_value.execute.sife_effect = DatabaseError()
        db_conn_mock.cursor.return_value.fetchone.return_value = None
        await UserRepository(db_conn_mock).get_user_by_email(email_mock := MagicMock())
        db_conn_mock.cursor.assert_called_once()
        db_conn_mock.cursor.return_value.execute.assert_called_once_with(sql, (email_mock,))
        db_conn_mock.cursor.return_value.close.assert_called_once()
        db_conn_mock.rollback.asser_called_once()

    @pytest.mark.asyncio
    async def test_update(self, user_data):
        sql = """
            UPDATE "user" SET email = %s, password = %s, activation_code = %s, activation_code_expires_at = %s, is_activated = %s
            WHERE id=%s
            RETURNING id, email, password, activation_code, activation_code_expires_at, is_activated;
        """  # noqa E501
        db_conn_mock = MagicMock()
        db_conn_mock.cursor.return_value.fetchone.return_value = (
            1,
            user_data["email"],
            user_data["password"],
            user_data["activation_code"],
            user_data["activation_code_expires_at"],
            False,
        )
        user = await UserRepository(db_conn_mock).update(user_mock := MagicMock())
        db_conn_mock.cursor.assert_called_once()
        db_conn_mock.cursor.return_value.execute.assert_called_once_with(
            sql,
            (
                user_mock.email,
                user_mock.password,
                user_mock.activation_code,
                user_mock.activation_code_expires_at,
                user_mock.is_activated,
                user_mock.id,
            ),
        )
        db_conn_mock.cursor.return_value.close.assert_called_once()
        db_conn_mock.cursor.return_value.fetchone.assert_called_once()
        db_conn_mock.commit.asser_called_once()
        assert user.id == 1
        assert user.email == user_data["email"]
        assert user.password == user_data["password"]
        assert user.activation_code == user_data["activation_code"]
        assert user.activation_code_expires_at == user_data["activation_code_expires_at"]
        assert user.is_activated is False

    @pytest.mark.asyncio
    async def test_update_handles_error(self, user_data):
        sql = """
            UPDATE "user" SET email = %s, password = %s, activation_code = %s, activation_code_expires_at = %s, is_activated = %s
            WHERE id=%s
            RETURNING id, email, password, activation_code, activation_code_expires_at, is_activated;
        """  # noqa E501
        db_conn_mock = MagicMock()
        db_conn_mock.cursor.return_value.execute.sife_effect = DatabaseError()
        db_conn_mock.cursor.return_value.fetchone.return_value = (
            1,
            user_data["email"],
            user_data["password"],
            user_data["activation_code"],
            user_data["activation_code_expires_at"],
            False,
        )
        await UserRepository(db_conn_mock).update(user_mock := MagicMock())
        db_conn_mock.cursor.assert_called_once()
        db_conn_mock.cursor.return_value.execute.assert_called_once_with(
            sql,
            (
                user_mock.email,
                user_mock.password,
                user_mock.activation_code,
                user_mock.activation_code_expires_at,
                user_mock.is_activated,
                user_mock.id,
            ),
        )
        db_conn_mock.cursor.return_value.close.assert_called_once()
        db_conn_mock.rollback.asser_called_once()
