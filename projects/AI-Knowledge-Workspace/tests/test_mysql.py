import os

from dotenv import load_dotenv
import pymysql


load_dotenv()

sql = """
    DESC users;
"""
try:
    connection = pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        charset="utf8mb4"
    )
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            data = cursor.fetchall()
            print(f"{'Field':<12} {'Type':<15} {'Null':<6} {'Key':<6} {'Default':<10} {'Extra'}")
            print('-'*65)
            for row in data:
                print(
                    f"{str(row[0]):<12}"
                    f"{str(row[1]):<15}"
                    f"{str(row[2]):<6}"
                    f"{str(row[3]):<6}"
                    f"{str(row[4]):<10}"
                    f"{str(row[5])}"
                )
except pymysql.MySQLError as e:
    print(f"MySQL error:{e}")

