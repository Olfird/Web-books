from loguru import logger
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.api.router import api_v1
from app.core.db import engine, async_session_maker
from app.modules.base.models import Base


async def create_db_and_tables():
    """Создание таблиц в базе данных"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Таблицы базы данных созданы")
    except Exception as e:
        logger.error(f"Ошибка при создании таблиц: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Запуск приложения...")
    await create_db_and_tables()
    logger.info("Приложение запущено")
    
    yield
    
    # Shutdown
    logger.info("Остановка приложения...")
    await engine.dispose()
    logger.info("Приложение остановлено")


app = FastAPI(
    title="Каталог прочитанных книг",
    description="Web-приложение для управления каталогом прочитанных книг",
    version="1.0.0",
    lifespan=lifespan
)

# Подключаем роутеры
app.include_router(api_v1)


@app.get("/")
async def root():
    return {"message": "Добро пожаловать в Каталог прочитанных книг!"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}