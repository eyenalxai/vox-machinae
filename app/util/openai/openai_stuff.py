from app.schema.openai import OpenAIResponse


def first_choice_text(openai_response: OpenAIResponse) -> str:
    return openai_response.choices[0].text
