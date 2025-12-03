from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserOut, UserWithBooksOut
from app.core.deps import get_db, get_db_with_commit
from app.core.security import get_token, decode_token
from .service import UserService
from .dao import UserDAO


router = APIRouter()


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_db),
) -> UserOut:
    """Dependency для получения текущего пользователя из токена"""
    token = get_token(request)
    payload = decode_token(token)
    user_id = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен"
        )
    
    user = await UserDAO.find_one_or_none_by_id(session, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    
    return UserOut(
        id=user.id,
        username=user.username,
        is_active=user.is_active
    )


@router.get("/me", response_model=UserWithBooksOut)
async def get_current_user_profile(
    current_user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_with_commit),
):
    svc = UserService(session)
    user_books = await svc.get_user_books(current_user.id)
    return UserWithBooksOut(
        **current_user.model_dump(),
        user_books=user_books
    )


@router.post("/me/books/{book_id}")
async def add_book_to_profile(
    book_id: int,
    current_user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_with_commit),
):
    svc = UserService(session)
    await svc.add_book_to_user(current_user.id, book_id)
    return {"success": True, "message": "Книга добавлена в профиль"}


@router.delete("/me/books/{book_id}")
async def remove_book_from_profile(
    book_id: int,
    current_user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_with_commit),
):
    svc = UserService(session)
    await svc.remove_book_from_user(current_user.id, book_id)
    return {"success": True, "message": "Книга удалена из профиля"}