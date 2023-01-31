import logging
from collections.abc import Callable

from httpx import HTTPStatusError

from app.app_settings import settings
from app.config.http_client import http_client
from app.schema.openai import OpenAIResponse
from app.util.openai.openai_stuff import first_choice_text


def openai_text_wrapper() -> Callable[[str], str]:
    url = "https://api.openai.com/v1/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {openai_token}".format(
            openai_token=settings.openai_token,
        ),
    }

    configuration = {
        "model": "text-davinci-003",
        "temperature": 0,
        "max_tokens": 512,
    }

    def text_prompt(message: str) -> str:
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
            return "An error occurred."
        except Exception as exception:
            logging.error(
                "Error: %s", exception  # noqa:  WPS323 Found `%` string formatting
            )
            return "An error occurred. Please try again."

        openai_response = OpenAIResponse(**response.json())

        return first_choice_text(openai_response=openai_response)

    return text_prompt
