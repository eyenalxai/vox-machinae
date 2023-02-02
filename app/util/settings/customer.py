from pydantic import BaseSettings, Field


class CustomerSettings(BaseSettings):
    openai_token: str = Field(..., env="OPENAI_TOKEN")
    settings_command = "settings"

    openai_api_url = "https://api.openai.com/v1"

    @property
    def openai_text_completion_url(self: "CustomerSettings") -> str:
        return "{api_url}/completions".format(
            api_url=self.openai_api_url,
        )

    @property
    def openai_image_generation_url(self: "CustomerSettings") -> str:
        return "{api_url}/images/generations".format(
            api_url=self.openai_api_url,
        )


customer_settings = CustomerSettings()
