from app.modules.base import BaseDAO
from .models import Book


class BookDAO(BaseDAO):
    model = Book