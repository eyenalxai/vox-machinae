import logging
from collections.abc import Callable

from httpx import HTTPStatusError

from app.config.http_client import http_client
from app.schema.openai import OpenAIResponse
from app.util.openai.openai_stuff import first_choice_text
from app.util.settings.customer import customer_settings


def openai_text_wrapper() -> Callable[[str], tuple[str, int]]:
    url = "https://api.openai.com/v1/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {openai_token}".format(
            openai_token=customer_settings.openai_token,
        ),
    }

    configuration = {
        "model": "text-davinci-003",
        "temperature": 0,
        "max_tokens": 512,
    }

    def text_prompt(message: str) -> tuple[str, int]:
        response = http_client.post(
            url=url,
            headers=headers,
            json={
                **configuration,
                "prompt": message,
            },
        )

        try:
            response.raise_for_status()
        except HTTPStatusError:
            logging.error("OpenAI API error: %s", response.text)
            raise
        except Exception as exception:
            logging.error(
                "Error: %s", exception  # noqa:  WPS323 Found `%` string formatting
            )
            raise

        openai_response = OpenAIResponse(**response.json())

        return (
            first_choice_text(openai_response=openai_response),
            openai_response.usage.total_tokens,
        )

    return text_prompt
