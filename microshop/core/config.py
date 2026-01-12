from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_v1_prefix: str = '/api/v1'

    db_url: str = Field(..., env='DB_URL')
    db_echo: bool = True

    # JWT
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    ALGORITHM: str = Field(..., env='ALGORITHM')


    class Config:
        env_file = '.env'


settings = Settings()
