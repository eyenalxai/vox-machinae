from typing import Literal

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    telegram_token: str = Field(..., env="TELEGRAM_TOKEN")

    poll_type: Literal["WEBHOOK", "POLLING"] = Field(..., env="POLL_TYPE")

    port: int = Field(..., env="PORT")
    domain: str = Field(..., env="DOMAIN")
    host: str = Field(env="HOST", default="0.0.0.0")
    main_bot_path: str = "/webhook/main"

    database_url: str = Field(..., env="DATABASE_URL")
    database_pool_size = 20

    @property
    def async_database_url(self: "Settings") -> str:
        return self.database_url.replace(
            "postgresql://",
            "postgresql+asyncpg://",
        )

    @property
    def webhook_url(self: "Settings") -> str:
        return "https://{domain}{main_bot_path}".format(
            domain=self.domain,
            main_bot_path=self.main_bot_path,
        )

    @validator("database_url")
    def domain_must_not_end_with_slash(
        cls: "Settings",
        v: str,
    ) -> str:

        if not v.startswith("postgresql://"):
            raise ValueError("DATABASE_URL must start with postgresql://")
        return v


settings = Settings()
