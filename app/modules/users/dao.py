from app.modules.base import BaseDAO
from .models import User, UserBook


class UserDAO(BaseDAO):
    model = User


class UserBookDAO(BaseDAO):
    model = UserBook