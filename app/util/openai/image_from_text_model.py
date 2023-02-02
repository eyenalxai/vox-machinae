from collections.abc import Callable
from typing import Literal

from app.schema.openai import OpenAIImageFromTextModelResponse
from app.util.openai.openai_stuff import first_url
from app.util.openai.send_request import send_openai_request
from app.util.settings.customer import customer_settings

TextModel = Literal[
    "text-davinci-003",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
]


def openai_image_from_text_model_wrapper() -> Callable[[str], tuple[str, int]]:
    url = customer_settings.openai_image_generation_url
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {openai_token}".format(
            openai_token=customer_settings.openai_token,
        ),
    }
    configuration: dict[str, str | int] = {
        "n": 1,
        "size": "1024x1024",
    }

    def image_from_text_model_prompt(prompt: str) -> tuple[str, int]:
        response = send_openai_request(
            url=url,
            headers=headers,
            configuration={
                **configuration,
            },
            prompt=prompt,
        )

        openai_response = OpenAIImageFromTextModelResponse(**response.json())

        return (
            first_url(openai_response=openai_response),
            1000,  # For 1024x1024 images
        )

    return image_from_text_model_prompt
