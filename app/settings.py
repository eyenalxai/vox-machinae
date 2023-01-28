from enum import Enum

from pydantic import BaseSettings, Field, validator


class PollType(Enum):
    WEBHOOK = "WEBHOOK"
    POLLING = "POLLING"


class Settings(BaseSettings):
    openai_token: str = Field(..., env="OPENAI_TOKEN")
    telegram_token: str = Field(..., env="TELEGRAM_TOKEN")

    # [1234567890, 1234567890, ...] # noqa: E800 Found commented out code
    allowed_user_ids: list[int] = Field(..., env="ALLOWED_USER_IDS")

    domain: str = Field(..., env="DOMAIN")
    port: int = Field(..., env="PORT")
    poll_type: PollType = Field(..., env="POLL_TYPE")
    main_bot_path: str = "/webhook/main"

    @property
    def webhook_url(self: "Settings") -> str:
        return "https://{domain}{main_bot_path}".format(
            domain=self.domain,
            main_bot_path=self.main_bot_path,
        )

    @validator("domain")
    def domain_must_not_end_with_slash(
        cls: "Settings",  # noqa: N805
        v: str,  # noqa: WPS111 Found too short name
    ) -> str:
        if v.endswith("/"):
            raise ValueError("Domain must not end with slash")

        if v.startswith("http://"):
            raise ValueError("Domain must not start with http://")

        return v


settings = Settings()
