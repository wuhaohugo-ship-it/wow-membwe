from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "WOW Members"
    ENV: str = "dev"
    BASE_URL: str = "http://localhost:8000"
    JWT_SECRET: str = Field(default="CHANGE_ME")
    JWT_ALG: str = "HS256"
    JWT_EXPIRES_MINUTES: int = 60 * 24 * 7
    DATABASE_URL: str = "postgresql+psycopg://wow:wowpass@localhost:5432/wow_members"
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
