import psycopg2
from fastapi import Depends

from entities.user import User
from utils.database import get_db_connection


class UserRepository:
    def __init__(self, db_conn=Depends(get_db_connection)):
        self.db_conn = db_conn

    async def save(self, user_data):
        sql = """
            INSERT INTO "user"(email, password, activation_code, activation_code_expires_at)
            VALUES(%s, %s, %s, %s)
            RETURNING id, email, password, activation_code, activation_code_expires_at;
        """
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(
                sql,
                (
                    user_data["email"],
                    user_data["password"],
                    user_data["activation_code"],
                    user_data["activation_code_expires_at"],
                ),
            )
        except psycopg2.DatabaseError as e:
            cursor.close()
            self.db_conn.rollback()
            raise e

        id, email, password, activation_code, activation_code_expires_at = cursor.fetchone()
        self.db_conn.commit()
        cursor.close()
        return User(id, email, password, activation_code, activation_code_expires_at)

    async def get_user_by_email(self, email):
        sql = """
            SELECT id, email, password, activation_code, activation_code_expires_at, is_activated
            FROM "user" WHERE email=%s
        """
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(sql, (email,))
        except psycopg2.DatabaseError as e:
            self.db_conn.rollback()
            raise e

        if (row := cursor.fetchone()) is not None:
            id, email, password, activation_code, activation_code_expires_at, is_activated = row
            user = User(
                id, email, password, activation_code, activation_code_expires_at, is_activated
            )
        else:
            user = None
        cursor.close()
        return user

    async def update(self, user: User):
        sql = """
            UPDATE "user" SET email = %s, password = %s, activation_code = %s, activation_code_expires_at = %s, is_activated = %s
            WHERE id=%s
            RETURNING id, email, password, activation_code, activation_code_expires_at, is_activated;
        """  # noqa: E501
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(
                sql,
                (
                    user.email,
                    user.password,
                    user.activation_code,
                    user.activation_code_expires_at,
                    user.is_activated,
                    user.id,
                ),
            )
        except psycopg2.DatabaseError as e:
            self.db_conn.rollback()
            raise e
        (
            id,
            email,
            password,
            activation_code,
            activation_code_expires_at,
            is_activated,
        ) = cursor.fetchone()
        self.db_conn.commit()
        cursor.close()
        return User(id, email, password, activation_code, activation_code_expires_at, is_activated)
