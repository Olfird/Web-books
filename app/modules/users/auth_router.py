from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_sessions
from app.core.security import get_password_hash, verify_password, create_access_token
from .dao import UserDAO
from .schemas import RegisterIn, LoginIn, TokenOut

router = APIRouter()


@router.post("/register")
async def register_user(
    user_data: RegisterIn,
    session: AsyncSession = Depends(db_sessions.get_db_with_commit),
) -> dict:
    user = await UserDAO.find_one_or_none(session, username=user_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    
    # Хэшируем пароль
    user_dict = user_data.model_dump()
    user_dict['hashed_password'] = get_password_hash(user_data.password)
    user_dict.pop('password')  # Удаляем plain password
    
    await UserDAO.add(session, **user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login", response_model=TokenOut)
async def login(
    response: Response,
    payload: LoginIn,
    session: AsyncSession = Depends(db_sessions.get_db)
):
    user = await UserDAO.get_by_username(session, payload.username)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные"
        )
    
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}