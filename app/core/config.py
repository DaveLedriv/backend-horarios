from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str = "change_me"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
