from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.core import db_sessions
from .models import User
from .service import UserService
from .schemas import UserOut, UserWithBooksOut


router = APIRouter()


@router.get('/me', response_model=UserWithBooksOut)
async def get_profile(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_sessions.get_db)
):
    svc = UserService(session)
    user_books = await svc.get_user_books(current_user.id)
    
    return UserWithBooksOut(
        id=current_user.id,
        username=current_user.username,
        is_active=current_user.is_active,
        user_books=user_books
    )


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