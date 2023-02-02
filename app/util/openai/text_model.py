from collections.abc import Callable
from typing import Literal

from app.schema.openai import OpenAITextModelResponse
from app.util.openai.openai_stuff import first_choice_text
from app.util.openai.send_request import send_openai_request
from app.util.settings.customer import customer_settings

TextModel = Literal[
    "text-davinci-003",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
]


def openai_text_model_wrapper() -> Callable[[str, TextModel], tuple[str, int]]:
    url = customer_settings.openai_text_completion_url
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

    def text_model_prompt(prompt: str, text_model: TextModel) -> tuple[str, int]:
        response = send_openai_request(
            url=url,
            headers=headers,
            configuration={**configuration, "model": text_model},
            prompt=prompt,
        )

        openai_response = OpenAITextModelResponse(**response.json())

        return (
            first_choice_text(openai_response=openai_response),
            openai_response.usage.total_tokens,
        )

    return text_model_prompt
