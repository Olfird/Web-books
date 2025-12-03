from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .dao import UserDAO, UserBookDAO
from .models import User, UserBook
from .schemas import UserCreate
from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, payload: UserCreate) -> User:
        # Проверяем, существует ли пользователь (только по username)
        if await UserDAO.find_one_or_none(self.session, username=payload.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким именем уже существует."
            )

        # Хэшируем пароль
        hashed_password = pwd_context.hash(payload.password)
        
        try:
            user_data = payload.model_dump()
            user_data['hashed_password'] = hashed_password
            user_data.pop('password')  # Удаляем plain password
            
            user = await UserDAO.add(self.session, **user_data)
            await self.session.commit()
            return user
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ошибка при создании пользователя."
            ) from e

    async def get_user_by_username(self, username: str) -> User:
        user = await UserDAO.find_one_or_none(self.session, username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден."
            )
        return user

    # Остальные методы остаются без изменений...
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
        return await UserBookDAO.find_all(self.session, user_id=user_id)

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)