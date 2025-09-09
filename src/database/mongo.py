from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
import src.models as models


class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = "mongodb://localhost:27017"
    DATABASE_NAME: Optional[str] = "people_finder_bot"

    # JWT
    secret_key: str = "secret"
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"
        from_attributes = True


settings = Settings()


async def initiate_database():
    print(settings.DATABASE_URL)
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    database = client[settings.DATABASE_NAME]
    await init_beanie(database=database, document_models=models.__all__)
