from app.schema.openai import OpenAIImageFromTextModelResponse, OpenAITextModelResponse


def first_choice_text(openai_response: OpenAITextModelResponse) -> str:
    return openai_response.choices[0].text


def first_url(openai_response: OpenAIImageFromTextModelResponse) -> str:
    return openai_response.data[0].url
