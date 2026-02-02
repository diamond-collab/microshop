from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    api_v1_prefix: str = '/api/v1'

    db_url: str = Field(..., validation_alias='DB_URL')
    db_echo: bool = True

    # JWT
    SECRET_KEY: str = Field(..., validation_alias='SECRET_KEY')
    ALGORITHM: str = Field(..., validation_alias='ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30


settings = Settings()
