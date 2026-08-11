import os
from dotenv import load_dotenv
import pymysql
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
load_dotenv()
password = os.getenv("MYSQL_PASSWORD")

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=6)
    age: int = Field(..., ge=18, le=100)


@app.post("/users")
def create_user(user: User):
    connection = pymysql.connect(
        host="localhost",
        port=33059,
        user="ruomo",
        password="123456",
        database="ai_workspace",
        charset="utf8mb4"
    )

    cursor = connection.cursor()

    sql = """
            INSERT INTO users (username, password, age)
            VALUES (%s, %s, %s)
        """

    cursor.execute(sql, (user.username, user.password, user.age))

    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message": "User created successfully",
        "username": user.username
    }
