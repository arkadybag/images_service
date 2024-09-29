import pydantic
from pydantic_settings import BaseSettings

pydantic.BaseSettings = BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    TEST_POSTGRES_DB: str = "test_db"

    class Config:
        env_file = ".env"
        extra = "ignore"
