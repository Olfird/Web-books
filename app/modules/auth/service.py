from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.modules.users.dao import UserDAO
from app.core.security import verify_password


class AuthService:
    @staticmethod
    async def authenticate_user(session: AsyncSession, username: str, password: str):
        """Аутентификация пользователя"""
        user = await UserDAO.find_one_or_none(session, username=username)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    @staticmethod
    async def get_current_user_from_token(token: str, session: AsyncSession):
        """Получение пользователя из токена"""
        from app.core.security import decode_token
        
        try:
            payload = decode_token(token)
            user_id = payload.get("sub")
            
            if user_id is None:
                return None
            
            user = await UserDAO.find_one_or_none_by_id(session, int(user_id))
            return user
        except Exception:
            return None