from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str = "change_me"
    ALGORITHM: str = "HS256"

    MAX_HORAS_CONTINUAS_DOCENTE: float = 4.0
    MAX_HORAS_DIARIAS_DOCENTE: float = 8.0
    MAX_HORAS_SEMANALES_DOCENTE: float = 15.0

    MAX_HORAS_CONTINUAS_GRUPO: float = 4.0
    MAX_HORAS_DIARIAS_GRUPO: float = 8.0
    MAX_HORAS_SEMANALES_GRUPO: float = 20.0

    class Config:
        env_file = ".env"


settings = Settings()
