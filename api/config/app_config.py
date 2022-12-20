from pydantic import BaseSettings, PostgresDsn

from config.enums import BestBetEnvironment


class AppSettings(BaseSettings):
    ENVIRONMENT: BestBetEnvironment
    DATABASE_URL: PostgresDsn
    JWT_SECRET: str
    MAILTRAP_API_KEY: str
    MAILTRAP_INBOX_NUMBER: int


AppConfig = AppSettings()
