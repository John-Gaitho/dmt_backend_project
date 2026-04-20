
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = 24
    UPLOAD_DIR: str = "./uploads"
    BASE_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"

settings = Settings()
