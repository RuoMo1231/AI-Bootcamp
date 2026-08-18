from fastapi import FastAPI, HTTPException, status
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.db import get_connection, execute_sql, get_user_sql, fetch_all, update_sql, delete_user_sql, DatabaseError

app = FastAPI()


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        sql = """
                INSERT INTO users (username, password, age)
                VALUES (%s, %s, %s)
            """
        params = (
            user.username,
            user.password,
            user.age
        )
        connection = get_connection()
        execute_sql(connection=connection, sql=sql, params=params)

        return {
            "message": "User created successfully",
            "username": user.username
        }

    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )


@app.get("/user/{user_id}")
def get_user(user_id: int) -> UserResponse:
    try:
        connection = get_connection()
        user_data = get_user_sql(
            connection=connection,
            user_id=user_id
        )
        if user_data is None:
            raise HTTPException(
                status_code=404,
                detail="404 NOT FOUND"
            )
        user_response = UserResponse(id=user_data[0], username=user_data[1], age=user_data[2])
        print(user_response)
        return user_response

    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )


@app.get("/users/{max_num}")
def get_users(max_num: int) -> list[UserResponse]:
    try:
        sql = """
            SELECT id,username,age FROM users LIMIT %s;
            """
        params = (max_num,)
        connection = get_connection()
        data = fetch_all(connection=connection, sql=sql, params=params)
        users_response = []
        for user_data in data:
            user_data = UserResponse(id=user_data[0], username=user_data[1], age=user_data[2])
            users_response.append(user_data)

        return users_response

    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )


@app.put("/update/{user_id}")
def update_user(user_id: int, user: UserUpdate) -> UserResponse:
    try:
        sql = """
            UPDATE users SET username=%s, age=%s WHERE id=%s
            """
        params = (user.username, user.age, user_id)
        connection = get_connection()
        update_status = update_sql(connection=connection, sql=sql, params=params)
        if update_status == 0:
            raise HTTPException(
                status_code=404,
                detail="404 NOT FOUND"
            )
        user_response = UserResponse(id=user_id, username=user.username, age=user.age)
        return user_response

    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )


@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    try:
        connection = get_connection()
        delete_status = delete_user_sql(
            connection=connection,
            user_id=user_id
        )

        if delete_status == 0:
            raise HTTPException(
                status_code=404,
                detail="404 NOT FOUND"
            )
        return {
            "message": "User Delete Successful",
            "user_id": user_id
        }

    except DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )
