from pydantic import BaseSettings, Field


class CustomerSettings(BaseSettings):
    openai_token: str = Field(..., env="OPENAI_TOKEN")
    options_command = "options"


customer_settings = CustomerSettings()
