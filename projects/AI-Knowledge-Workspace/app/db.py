import os
from dotenv import load_dotenv
import pymysql

load_dotenv()


class DatabaseError(Exception):
    pass


def get_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            charset="utf8mb4"
        )

        return connection

    except pymysql.MySQLError as e:
        print(f"MySQL Connection:{e}")
        raise DatabaseError("Database connection failed") from e


def execute_sql(connection, sql, params):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                connection.commit()
                connection.close()

    except pymysql.MySQLError as e:
        print(f"MySQL Execute Error:{e}")
        raise DatabaseError("Database operation failed") from e


def fetch_one(connection, sql, params):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                data = cursor.fetchone()
                connection.close()
                return data

    except pymysql.MySQLError as e:
        print(f"MySQL Execute Error:{e}")
        raise DatabaseError("Database operation failed") from e


def fetch_all(connection, sql, params):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                data = cursor.fetchall()
                connection.close()
                return data

    except pymysql.MySQLError as e:
        print(f"MySQL Execute Error:{e}")
        raise DatabaseError("Database operation failed") from e


def update_sql(connection, sql, params):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                connection.commit()
                update_status = cursor.rowcount
                connection.close()
                return update_status

    except pymysql.MySQLError as e:
        print(f"MySQL Execute Error:{e}")
        raise DatabaseError("Database operation failed") from e


def delete_sql(connection, sql, params):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                connection.commit()
                delete_status = cursor.rowcount
                connection.close()
                return delete_status

    except pymysql.MySQLError as e:
        print(f"MySQL Execute Error:{e}")
        raise DatabaseError("Database operation failed") from e
