import os
import json
from dotenv import load_dotenv
import pymysql
import redis

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


def get_client():
    try:
        client = redis.Redis(
            host="127.0.0.1",
            port=63790,
            decode_responses=True
        )

        return client

    except redis.RedisError as e:
        print(f"Redis Client Error:{e}")
        raise DatabaseError("Redis client failed") from e


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


def get_user_cache(user_id):
    key = f"user:{user_id}"
    client = get_client()
    try:
        data = client.get(key)
    except redis.RedisError as e:
        print(f"Redis GET Error:{e}")
        data = get_user_sql(user_id=user_id)
        if data is not None:
            data = {
                "id": data[0],
                "username": data[1],
                "age": data[2]
            }
            return data
        return data
    else:
        if data is not None:
            return json.loads(data)
        data = get_user_sql(user_id=user_id)
        if data is None:
            return data
        data = {
            "id": data[0],
            "username": data[1],
            "age": data[2]
        }
        json_data = json.dumps(data)
        try:
            client.set(key, json_data, ex=60)
        except redis.RedisError as e:
            print(f"Redis SET Error:{e}")
            return data
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


def get_users_cache():
    pass


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


def update_user_cache(user_id, user):
    key = f"user:{user_id}"

    update_status = update_user_sql(
        username=user.username,
        age=user.age,
        user_id=user_id
    )
    if update_status == 0:
        return update_status
    client = get_client()
    data = {
        "id": user_id,
        "username": user.username,
        "age": user.age
    }
    json_data = json.dumps(data)
    try:
        client.set(key, json_data, ex=60)
    except redis.RedisError as e:
        print(f"Redis SET Error:{e}")
        try:
            client.delete(key)
        except redis.RedisError as delete_error:
            print(f"Redis DEL Error:{delete_error}")
        return 1
    else:
        return 1


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


def delete_user_cache(user_id):
    key = f"user:{user_id}"
    delete_status = delete_user_sql(user_id=user_id)
    if delete_status == 0:
        return delete_status
    client = get_client()
    try:
        client.delete(key)
    except redis.RedisError as e:
        print(f"Redis DEL Error:{e}")
        return delete_status
    else:
        return delete_status
