from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME:str = "FocusFlow"
    VERSION:str = "0.1.0"
    
    SECRET_KEY:str 
    ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 30
    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int 
    POSTGRES_DB: str
    
    @property
    def DATABASE_URL(self) -> str:
        
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )  
    
settings = Settings()