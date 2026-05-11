from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKER_COUNT: int = 2
    KEEPALIVE_SECONDS: int = 5

    DEFAULT_STATUS_CODE: int = 200
    TIMEOUT_SECONDS: int = 30
    MAX_PAYLOAD_BYTES: int = 1_048_576
    ENABLE_DEBUG: bool = False
    ENABLE_GZIP: bool = True

    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_JSON: bool = True

    MOCK_AUTH_TOKEN: str = "test-token-12345"

    RATE_LIMIT_GLOBAL: str = "500/minute"
    RATE_LIMIT_PER_IP: str = "100/minute"
    RATE_LIMIT_AUTH: str = "20/minute"

    ALLOWED_HEADERS: str = "Authorization,Content-Type,X-Request-ID,X-Scenario,X-Debug-Mode"

    SCENARIOS_FILE: str = "app/engine/scenarios.yaml"
    SCENARIOS_HOT_RELOAD: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
