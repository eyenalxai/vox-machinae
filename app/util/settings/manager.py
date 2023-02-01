from pydantic import BaseSettings, Field


class ManagerSettings(BaseSettings):
    # Example: [1234567890, 1234567890, ...] # noqa: E800 Found commented out code
    admin_user_ids: list[int] = Field(..., env="ADMIN_USER_IDS")


manager_settings = ManagerSettings()
