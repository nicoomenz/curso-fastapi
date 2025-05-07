from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    admin_username: str
    admin_password: str

    class Config:
        env_file = ".env"

settings = Settings()
