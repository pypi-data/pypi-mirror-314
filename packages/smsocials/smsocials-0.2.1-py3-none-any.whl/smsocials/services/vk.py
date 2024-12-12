from typing import Any, Dict

import aiohttp

from ..clients.vk import VKClient


class VKService:
    def __init__(self, token: str):
        self.token = token
        self.session = lambda: aiohttp.ClientSession()

    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        async with self.session() as session:
            vk_client = VKClient(session, self.token)
            result = await vk_client.get_account_info(user_id)
            return result
