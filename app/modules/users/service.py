from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from fastapi import HTTPException, status

from .dao import UserBookDAO
from .models import UserBook
from app.modules.books_catalog.models import Book


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_book_to_user(self, user_id: int, book_id: int) -> UserBook:
        # Проверяем, не добавлена ли книга уже
        existing = await UserBookDAO.find_one_or_none(
            self.session, user_id=user_id, book_id=book_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Книга уже добавлена в ваш профиль."
            )

        try:
            user_book = await UserBookDAO.add(
                self.session, user_id=user_id, book_id=book_id
            )
            await self.session.commit()
            return user_book
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка при добавлении книги."
            ) from e

    async def remove_book_from_user(self, user_id: int, book_id: int) -> bool:
        deleted_count = await UserBookDAO.delete(
            self.session, user_id=user_id, book_id=book_id
        )
        if deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Книга не найдена в вашем профиле."
            )
        await self.session.commit()
        return True

    async def get_user_books(self, user_id: int) -> list[UserBook]:
        # Загружаем UserBook вместе с данными книги
        result = await self.session.execute(
            select(UserBook)
            .options(joinedload(UserBook.book))
            .where(UserBook.user_id == user_id)
        )
        return result.scalars().all()