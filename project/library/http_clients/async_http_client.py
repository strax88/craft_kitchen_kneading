from typing import Any

from httpx import AsyncClient, Headers, URL


class AsyncHTTPClient:

    _client: AsyncClient = None

    def __init__(self, base_url: str | None = None, headers: dict | None = None) -> None:
        """"""
        params = {"verify": False} # todo: решить вопрос с сертификатами
        if base_url: params["base_url"] = base_url
        if headers: params["headers"] = headers
        self.client = AsyncClient(**params)

    @property
    def client(self) -> AsyncClient:
        """"""
        return self._client

    @client.setter
    def client(self, value: AsyncClient):
        """"""
        self._client = value

    @property
    def base_url(self) -> URL:
        """"""
        return self.client.base_url

    @base_url.setter
    def base_url(self, value) -> None:
        """"""
        base_url = URL(url=value)
        self.client.base_url = base_url

    @property
    def headers(self) -> dict | Headers:
        """"""
        return self.client.headers

    @headers.setter
    def headers(self, value) -> None:
        """"""
        headers = Headers(headers=value)
        self.client.headers = headers

    async def get(self, endpoint: str, headers: dict | None = None, **kwargs) -> Any:
        """"""
        if headers:
            self.headers = headers
        async with self.client as web_client:
            """"""
            response = await web_client.get(endpoint, **kwargs)
            return response.json()

    async def post(self, endpoint: str, data: Any | None = None, headers: dict | None = None, **kwargs) -> Any:
        """"""
        if headers:
            self.headers = headers
        async with self.client as web_client:
            """"""
            response = await web_client.post(endpoint, json=data, **kwargs)
            return response.json()
