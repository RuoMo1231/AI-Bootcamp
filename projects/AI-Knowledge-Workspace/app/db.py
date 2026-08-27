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
        with connection.cursor() as cursor:
            cursor.execute(sql, params)

    except pymysql.MySQLError as e:
        print(f"MySQL Execute Error:{e}")
        raise DatabaseError("Database operation failed") from e


def create_user_sql(username, password, age):
    connection = get_connection()
    sql = """
            INSERT INTO users(username,password,age)
            VALUES(%s,%s,%s)
        """
    params = (username, password, age)
    try:
        with connection:
            execute_sql(connection=connection, sql=sql, params=params)
            connection.commit()

    except pymysql.MySQLError as e:
        print(f"MySQL Commit Error:{e}")
        raise DatabaseError("Database commit failed") from e


def fetch_one(connection, sql, params):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            data = cursor.fetchone()
            return data

    except pymysql.MySQLError as e:
        print(f"MySQL Execute Error:{e}")
        raise DatabaseError("Database operation failed") from e


def get_user_sql(user_id):
    connection = get_connection()
    sql = """
            SELECT id,username,age FROM users WHERE id=%s;
        """
    params = (user_id,)
    try:
        with connection:
            data = fetch_one(connection=connection, sql=sql, params=params)
    except pymysql.MySQLError as e:
        print(f"MySQL Commit Error:{e}")
        raise DatabaseError("Database commit failed") from e
    return data


def fetch_all(connection, sql, params):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            data = cursor.fetchall()
            return data

    except pymysql.MySQLError as e:
        print(f"MySQL Execute Error:{e}")
        raise DatabaseError("Database operation failed") from e


def get_users_sql(max_num):
    connection = get_connection()
    sql = """
        SELECT id,username,age FROM users LIMIT %s;
        """
    params = (max_num,)
    try:
        with connection:
            data = fetch_all(connection=connection, sql=sql, params=params)

    except pymysql.MySQLError as e:
        print(f"MySQL Commit Error:{e}")
        raise DatabaseError("Database commit failed") from e
    
    return data


def update_sql(connection, sql, params):
    try:

        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            update_status = cursor.rowcount
            return update_status

    except pymysql.MySQLError as e:
        print(f"MySQL Execute Error:{e}")
        raise DatabaseError("Database operation failed") from e


def update_user_sql(username, age, user_id):
    connection = get_connection()
    sql = """
        UPDATE users SET username=%s,age=%s WHERE id=%s;
        """
    params = (username, age, user_id)
    try:
        with connection:
            update_status = update_sql(connection=connection, sql=sql, params=params)
            connection.commit()

    except pymysql.MySQLError as e:
        print(f"MySQL Commit Error:{e}")
        raise DatabaseError("Database commit failed") from e

    return update_status


def delete_sql(connection, sql, params):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            connection.commit()
            delete_status = cursor.rowcount
            return delete_status

    except pymysql.MySQLError as e:
        print(f"MySQL Execute Error:{e}")
        raise DatabaseError("Database operation failed") from e


def delete_user_sql(user_id: int):
    connection = get_connection()
    sql = """
            DELETE FROM users WHERE id=%s;
        """
    params = (user_id,)
    try:
        with connection:
            delete_status = delete_sql(connection=connection, sql=sql, params=params)
            connection.commit()

    except pymysql.MySQLError as e:
        print(f"MySQL Commit Error:{e}")
        raise DatabaseError("Database commit failed") from e

    return delete_status
