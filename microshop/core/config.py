from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_v1_prefix: str = '/api/v1'

    db_url: str = Field(..., env='DB_URL')
    db_echo: bool = True

    # JWT
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    ALGORITHM: str = Field(..., env='ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    class Config:
        env_file = '.env'


settings = Settings()
