from app.config.pydantic import Immutable


class Choice(Immutable):
    text: str


class Usage(Immutable):
    total_tokens: int


class OpenAIResponse(Immutable):
    id: str
    object: str
    choices: list[Choice]
    usage: Usage
