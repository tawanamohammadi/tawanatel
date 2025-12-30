import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    BOT_TOKEN: str = "8425921084:AAFRFLHDE73mwq15zf91unNQ7__ctHvFusQ"
    TTC_API_KEY: str = "" # User needs to provide this
    DATABASE_URL: str = "sqlite+aiosqlite:///data/database.db"
    
    # API Settings
    TTC_BASE_URL: str = "https://hero-sms.com/stubs/handler_api.php"
    
    # Bot Settings
    ADMIN_IDS: list[int] = [12345678] # Add admin IDs here
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
