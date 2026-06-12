from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 1. Provide types and validation rules
    DATABASE_URL: str
    
    # 2. Instruct Pydantic to read from your local file
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" # Safely bypasses other env vars on your computer
    )

# Instantiate as a reusable singleton object
Config = Settings()
