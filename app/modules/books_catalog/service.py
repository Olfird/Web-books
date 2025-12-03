from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .dao import BookDAO
from .models import Book
from .schemas import BookCreate
from fastapi import HTTPException, status


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_book(self, payload: BookCreate) -> Book:
        try:
            book = await BookDAO.add(self.session, **payload.model_dump())
            await self.session.commit()
            return book
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Книга с таким названием уже существует."
            ) from e
        except Exception:
            await self.session.rollback()
            raise

    async def list_books(self) -> list[Book]:
        return await BookDAO.find_all(self.session)

    async def get_book(self, book_id: int) -> Book:
        book = await BookDAO.find_one_or_none_by_id(self.session, book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Книга не найдена."
            )
        return book