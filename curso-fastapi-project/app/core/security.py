from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Mi App"
    debug: bool = True
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()