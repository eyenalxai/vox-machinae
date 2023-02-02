from app.config.pydantic import Immutable


class Choice(Immutable):
    text: str


class Usage(Immutable):
    total_tokens: int


class OpenAITextModelResponse(Immutable):
    id: str
    object: str
    choices: list[Choice]
    usage: Usage


class ImageUrl(Immutable):
    url: str


class OpenAIImageFromTextModelResponse(Immutable):
    created: int
    data: list[ImageUrl]
