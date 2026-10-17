from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    deribit_url: str = "https://test.deribit.com/api/v2"
    database_url: str = Field(default=...)
    redis_url: str = Field(default=...)

    debug: bool = False
    show_docs: bool = False
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
