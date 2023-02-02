from app.util.openai.text_model import TextModel


def text_model_from_state_value(
    state_value: str | None,
) -> TextModel:
    if state_value == "TextModelSG:davinci":
        return "text-davinci-003"

    if state_value == "TextModelSG:curie":
        return "text-curie-001"

    if state_value == "TextModelSG:babbage":
        return "text-babbage-001"

    if state_value == "TextModelSG:ada":
        return "text-ada-001"

    raise NotImplementedError(
        "State {state_value} is not implemented".format(state_value=state_value),
    )
