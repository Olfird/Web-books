from app.modules.base import Base
from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.users.models import UserBook


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)


    # Связь с пользователями, которые добавили книгу
    user_books: Mapped[List["UserBook"]] = relationship(
        back_populates="book",
        lazy="selectin",
    )