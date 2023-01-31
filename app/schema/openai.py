from app.config.pydantic import Immutable


class Choice(Immutable):
    index: int
    text: str


class OpenAIResponse(Immutable):
    id: str
    object: str
    created: int
    model: str
    choices: list[Choice]
