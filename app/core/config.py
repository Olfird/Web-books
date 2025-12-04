import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):
    # Database
    POSTGRES_DRIVER: str = "postgresql+asyncpg"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "14789632"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DBNAME: str = "book_catalog"

    @computed_field(return_type=str)
    @property
    def DB_URL(self) -> str:
        return (
            f"{self.POSTGRES_DRIVER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DBNAME}"
        )

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    
    ###########################
    # ПУТИ
    ###########################
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ENV_DIR: str = os.path.join(BASE_DIR, ".env")
    LOGS_DIR: str = os.path.join(BASE_DIR, "logs/")

    model_config = SettingsConfigDict(
        env_file=ENV_DIR
    )

# Инициализация настроек
settings = Settings()
database_url = settings.DB_URL

def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}