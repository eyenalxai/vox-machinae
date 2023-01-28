from httpx import Client, Timeout

timeout = Timeout(60.0, connect=60.0, read=60.0)
http_client = Client(timeout=timeout)
