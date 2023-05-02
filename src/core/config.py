from pydantic import BaseSettings, AnyHttpUrl
from decouple import config
from typing import List


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_SECRET_REFRESH_KEY: str = config("JWT_SECRET_REFRESH_KEY", cast=str)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60
    BACKEND_CORS_ORIGIN: List[AnyHttpUrl] = []
    PROJECT_NAME: str = "WEATHERAPI"

    # Database
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)


    class Config:
        case_sensitive = True


settings = Settings()
