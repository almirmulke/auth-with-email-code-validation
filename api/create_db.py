from utils.database import db_conn


def main():
    cursor = db_conn.cursor()

    cursor.execute(
        """
        CREATE table if not exists "user" (
            id bigint primary key GENERATED ALWAYS AS IDENTITY,
            email varchar(256) unique not null,
            activation_code smallint,
            password varchar(256) not null,
            activation_code_expires_at timestamp,
            is_activated bool not null default false
        );
        """
    )
    db_conn.commit()
    cursor.close()


if __name__ == "__main__":
    main()
