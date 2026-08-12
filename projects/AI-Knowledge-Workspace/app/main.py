from fastapi import FastAPI, HTTPException, status
from app.schemas import UserCreate
from app.db import get_connection, execute_sql, DatabaseError

app = FastAPI()


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        connection = get_connection()
        params = (
            user.username,
            user.password,
            user.age
        )
        sql = """
                INSERT INTO users (username, password, age)
                VALUES (%s, %s, %s)
            """
        execute_sql(
            connection=connection,
            sql=sql,
            params=params
        )

        return {
            "message": "User created successfully",
            "username": user.username
        }

    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )
