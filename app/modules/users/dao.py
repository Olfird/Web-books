from app.modules.base import BaseDAO
from .models import User, UserBook

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_by_username(cls, session: AsyncSession, username: str) -> User | None:
        res = await session.execute(select(User).where(User.username == username))
        return res.scalar_one_or_none()


class UserBookDAO(BaseDAO):
    model = UserBook