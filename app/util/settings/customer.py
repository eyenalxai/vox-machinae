from pydantic import BaseSettings, Field


class CustomerSettings(BaseSettings):
    openai_token: str = Field(..., env="OPENAI_TOKEN")


customer_settings = CustomerSettings()
