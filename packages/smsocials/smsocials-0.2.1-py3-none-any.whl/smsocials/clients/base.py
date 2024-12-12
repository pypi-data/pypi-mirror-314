from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseClient(ABC):
    @abstractmethod
    async def request(self, method: str, **data: Any) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_account_info(
        self, account_id: str, **data: Any
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def create_resource(self, name: str, **data: Any) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def create_post(self, **data: Any) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def upload_video(self, path: str, **data: Any) -> Dict[str, Any]:
        pass
