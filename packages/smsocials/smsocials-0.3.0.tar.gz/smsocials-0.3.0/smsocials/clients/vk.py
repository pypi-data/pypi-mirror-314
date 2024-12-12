from typing import Any, Dict

import aiohttp

from .base import BaseClient


class VKClient(BaseClient):
    def __init__(self, session: aiohttp.ClientSession, token: str):
        self.session = session
        self.token = token
        self.api_url = "https://api.vk.com/method/"
        self.api_version = "5.131"

    async def request(self, method: str, **data: Any) -> Dict[str, Any]:
        data["access_token"] = self.token
        data["v"] = self.api_version
        async with self.session.get(
            f"{self.api_url}{method}", params=data
        ) as response:
            response_data = await response.json()
            return response_data.get("response", {})

    async def get_account_info(
        self, account_id: str, **data: Any
    ) -> Dict[str, Any]:
        data["user_ids"] = account_id
        response = await self.request("users.get", **data)
        return response

    async def create_resource(self, name: str, **data: Any) -> Dict[str, Any]:
        return {"": ""}

    async def create_post(self, **data: Any) -> Dict[str, Any]:
        return {"": ""}

    async def upload_video(self, path: str, **data: Any) -> Dict[str, Any]:
        return {"": ""}
