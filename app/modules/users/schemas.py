from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime


class UserBase(BaseModel):
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool


class UserBookOut(BaseModel):
    id: int
    book_id: int
    user_id: int
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserWithBooksOut(UserOut):
    user_books: List[UserBookOut] = []