from moy_nalog.http import HttpConnection


class BaseAPI:
    def __init__(self, connection: HttpConnection) -> None:
        self.connection = connection

    async def _get_bearer_auth_header(self) -> dict:
        return await self.connection.auth.get_bearer_auth_header()

    async def get(self, url: str, **kwargs) -> dict:
        response = await self.connection.client.get(
            url=url, headers=await self._get_bearer_auth_header(), **kwargs
        )
        return response.json()

    async def post(self, url: str, json: dict, **kwargs) -> dict:
        response = await self.connection.client.post(
            url=url, json=json, headers=await self._get_bearer_auth_header(), **kwargs
        )
        return response.json()
