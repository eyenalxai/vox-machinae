from pydantic import BaseSettings, Field


class CustomerSettings(BaseSettings):
    openai_token: str = Field(..., env="OPENAI_TOKEN")
    settings_command = "settings"


customer_settings = CustomerSettings()
