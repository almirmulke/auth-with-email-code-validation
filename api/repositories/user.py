import psycopg2

from entities.user import User
from utils.database import db_conn


class UserRepository:
    async def save(self, user_data):
        sql = """
            INSERT INTO "user"(email, password, activation_code, activation_code_expires_at)
            VALUES(%s, %s, %s, %s)
            RETURNING id, email, password, activation_code, activation_code_expires_at;
        """
        cursor = db_conn.cursor()
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
            db_conn.rollback()
            raise e

        id, email, password, activation_code, activation_code_expires_at = cursor.fetchone()
        db_conn.commit()
        cursor.close()
        return User(id, email, password, activation_code, activation_code_expires_at)

    async def get_user_by_email(self, email):
        sql = """
            SELECT id, email, password, activation_code, activation_code_expires_at, is_activated
            FROM "user" WHERE email=%s
        """
        cursor = db_conn.cursor()
        try:
            cursor.execute(sql, (email,))
        except psycopg2.DatabaseError as e:
            db_conn.rollback()
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
        cursor = db_conn.cursor()
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
            db_conn.rollback()
            raise e
        (
            id,
            email,
            password,
            activation_code,
            activation_code_expires_at,
            is_activated,
        ) = cursor.fetchone()
        db_conn.commit()
        cursor.close()
        return User(id, email, password, activation_code, activation_code_expires_at, is_activated)
