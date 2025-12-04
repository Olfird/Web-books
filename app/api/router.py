from fastapi import APIRouter

from app.modules.users import router as user_router, auth_router
from app.modules.books_catalog import router as books_router

router = APIRouter(prefix='/api/v1', tags=['FavoriteWorks API V1'])

router.include_router(user_router, prefix='/users', tags=['Users'])
router.include_router(books_router, prefix='/books_catalog', tags=['Books_catalog'])
router.include_router(auth_router, prefix='/auth', tags=["Auth"])