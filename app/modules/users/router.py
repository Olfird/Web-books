from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from app.core.deps import get_current_user
from app.core import db_sessions
from .models import User, UserBook
from .service import UserService
from .schemas import UserOut, UserWithBooksOut


router = APIRouter()


@router.get('/me', response_model=UserWithBooksOut)
async def get_profile(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_sessions.get_db)
):
    # Получаем пользователя с его книгами и данными книг
    result = await session.execute(
        select(User)
        .options(
            selectinload(User.user_books)
            .joinedload(UserBook.book)
        )
        .where(User.id == current_user.id)
    )
    
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    return user


@router.post('/me/books/{book_id}')
async def add_book_to_profile(
    book_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_sessions.get_db_with_commit)
):
    svc = UserService(session)
    await svc.add_book_to_user(current_user.id, book_id)
    return {"success": True, "message": "Книга добавлена в профиль"}


@router.delete('/me/books/{book_id}')
async def remove_book_from_profile(
    book_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_sessions.get_db_with_commit)
):
    svc = UserService(session)
    await svc.remove_book_from_user(current_user.id, book_id)
    return {"success": True, "message": "Книга удалена из профиля"}