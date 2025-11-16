# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    # These values will be read from the environment
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    # We construct the DATABASE_URL from the other vars
    DATABASE_URL: str = ""

    # This logic constructs the URL *after* loading the env vars
    def __init__(self, **values):
        super().__init__(**values)
        self.DATABASE_URL = (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@db:5432/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()