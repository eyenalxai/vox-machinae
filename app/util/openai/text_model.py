import logging
from collections.abc import Callable
from typing import Literal

from httpx import HTTPStatusError

from app.config.http_client import http_client
from app.schema.openai import OpenAIResponse
from app.util.openai.openai_stuff import first_choice_text
from app.util.settings.customer import customer_settings

TextModel = Literal[
    "text-davinci-003",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
]


def openai_text_wrapper() -> Callable[[str, TextModel], tuple[str, int]]:
    url = "https://api.openai.com/v1/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {openai_token}".format(
            openai_token=customer_settings.openai_token,
        ),
    }

    configuration = {
        "temperature": 0,
        "max_tokens": 512,
    }

    def text_prompt(prompt: str, text_model: TextModel) -> tuple[str, int]:
        response = http_client.post(
            url=url,
            headers=headers,
            json={
                **configuration,
                "model": text_model,
                "prompt": prompt,
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
