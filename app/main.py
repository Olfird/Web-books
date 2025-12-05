from loguru import logger

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.core.config import settings
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):    
    try:
        logger.info("Startup: Completed")
        yield
    finally:
        logger.info("Shutdown: Completed")


app = FastAPI(
    title="Каталог прочитанных книг",
    description="Web-приложение для управления каталогом прочитанных книг",
    version="1.0.0",
    lifespan=lifespan
)

# Настройка CORS
# Определяем разрешенные источники - включаем все возможные варианты localhost
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

if hasattr(settings, 'FRONT_SITE') and settings.FRONT_SITE:
    if isinstance(settings.FRONT_SITE, str):
        if settings.FRONT_SITE not in allowed_origins:
            allowed_origins.append(settings.FRONT_SITE)
    else:
        allowed_origins.extend(settings.FRONT_SITE)

logger.info(f"CORS allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы включая OPTIONS
    allow_headers=["*"],  # Разрешаем все заголовки
    expose_headers=["*"],
    max_age=3600,  # Кэширование preflight запросов на 1 час
)

app.include_router(api_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Базовые эндпоинты
@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в Каталог прочитанных книг!",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Эндпоинт для проверки здоровья приложения"""
    return {
        "status": "healthy",
        "service": "Каталог прочитанных книг"
    }