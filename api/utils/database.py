import psycopg2

db_conn = psycopg2.connect(
    database="", host="postgres", user="postgres", password="not-secret", port="5432"
)
