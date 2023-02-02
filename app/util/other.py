from app.util.openai.text_model import TextModel


def pretty_text_model_name(text_model: TextModel) -> str:
    if text_model == "text-davinci-003":
        return "Davinci"

    if text_model == "text-curie-001":
        return "Curie"

    if text_model == "text-babbage-001":
        return "Babbage"

    if text_model == "text-ada-001":
        return "Ada"

    raise NotImplementedError(
        "Text model {text_model} is not implemented".format(text_model=text_model),
    )
