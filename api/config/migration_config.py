from pydantic import BaseSettings, PostgresDsn

from config.enums import BestBetEnvironment


class MigrationSettings(BaseSettings):
    ENVIRONMENT: BestBetEnvironment
    DATABASE_URL: PostgresDsn


MigrationConfig = MigrationSettings()
