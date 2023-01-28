from aiohttp.web_request import Request
from aiohttp.web_response import Response


async def health(_request: Request) -> Response:
    return Response()
