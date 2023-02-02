from app.config.pydantic import Immutable


class Choice(Immutable):
    text: str


class OpenAIResponse(Immutable):
    id: str
    object: str
    choices: list[Choice]
