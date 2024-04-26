from pydantic_settings import BaseSettings
import os 
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    class Config: 
        env_file = '.env'
        extra = 'ignore'  
    
    DOCS_USERNAME: str = 'jakubkubala'
    DOCS_PASSWORD: str = '12345'
    LOG_LEVEL: str = 'DEBUG'
    APP_VERSION: str = os.getenv("APP_VERSION")
    APP_PORT: int = 8833
    APP_ROOT_PATH: str = os.getenv("APP_ROOT_PATH")

    BEARER_TOKEN: str = 'random-token'

    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")


settings = Settings()