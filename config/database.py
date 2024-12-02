import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    DB_NAME: str
    ENV: str
    HOST: str
    PORT: int

    class Config:
        env_file = ".env" # Default env file

def load_settings():
    env = os.getenv("ENV")

    if env == "PRODUCTION":
        Settings.Config.env_file = ".env.prod"
    else:
        Settings.Config.env_file = ".env.dev"
    return Settings()

settings = load_settings()