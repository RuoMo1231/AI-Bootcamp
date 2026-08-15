from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str
    password: str
    age: int


class UserResponse(BaseModel):
    id: int
    username: str
    age: int


class UserUpdate(BaseModel):
    username: str | None = None
    age: int | None = None
