from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Task Optimizer API"
    app_env: str = "development"
    database_url: str = "postgresql+psycopg2://task_optimizer:task_optimizer@localhost:5432/task_optimizer"
    cors_origins: str = "http://localhost:5173,http://localhost:5174"
    hr_alert_webhook: str = ""
    stress_streak_threshold: int = 2

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
