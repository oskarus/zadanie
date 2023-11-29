from pydantic_settings import BaseSettings
import os

class AppConfig(BaseSettings):
    app_name: str = "Zadanie"
    debug: bool = os.environ.get("DEBUG","True").lower() == 'true'
    postgres_db: str = os.environ.get("POSTGRES_DB","zadanie")
    postgres_user: str = os.environ.get("POSTGRES_USER", "user")
    postgres_password: str = os.environ.get("POSTGRES_PASSWORD", "password")
    database_url: str = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@db/{postgres_db}"

config = AppConfig()
