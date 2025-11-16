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
    
    # --- ADD THESE LINES for Redis/Celery ---
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    
    CELERY_BROKER_URL: str = ""
    CELERY_RESULT_BACKEND_URL: str = ""
    # --- END ADD ---

    def __init__(self, **values):
        super().__init__(**values)
        
        # --- UPDATE THIS ---
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql+asyncpg://"
                f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@db:5432/{self.POSTGRES_DB}"
            )
        
        # --- ADD THIS LOGIC ---
        if not self.CELERY_BROKER_URL:
            self.CELERY_BROKER_URL = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"
            
        if not self.CELERY_RESULT_BACKEND_URL:
            self.CELERY_RESULT_BACKEND_URL = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/1"
        # --- END ADD ---

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()