from fastapi import APIRouter

from app.modules.users.router import router as user_router
from app.modules.books_catalog.router import router as books_router
from app.modules.auth.router import router as auth_router


api_v1 = APIRouter(prefix='/api/v1', tags=['FavoriteWorks API V1'])

# include-ы
api_v1.include_router(user_router, prefix='/users', tags=['users'])
api_v1.include_router(books_router, prefix='/books_catalog', tags=['books_catalog'])
api_v1.include_router(auth_router, prefix='/auth', tags=["auth"])