from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class RegisterIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=6, max_length=128)


class LoginIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=6, max_length=128)


class TokenOut(BaseModel):
    access_token: str


class UserOut(BaseModel):
    id: int
    username: str
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


class UserBookOut(BaseModel):
    id: int
    book_id: int
    user_id: int
    added_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserWithBooksOut(UserOut):
    user_books: List[UserBookOut] = []