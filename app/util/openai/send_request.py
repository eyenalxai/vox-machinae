from httpx import HTTPStatusError, Response

from app.config.http_client import http_client
from app.config.log import logger


def send_openai_request(
    url: str,
    headers: dict[str, str],
    configuration: dict[str, str | int],
    prompt: str,
) -> Response:
    response = http_client.post(
        url=url,
        headers=headers,
        json={
            **configuration,
            "prompt": prompt,
        },
    )

    try:
        response.raise_for_status()
    except HTTPStatusError as http_status_error:
        logger.error("OpenAI API error: %s", http_status_error)
        raise
    except Exception as exception:
        logger.error(
            "Error: %s", exception  # noqa:  WPS323 Found `%` string formatting
        )
        raise

    return response
