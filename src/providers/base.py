from abc import ABC, abstractmethod
from typing import Any, Type, Union

Class = Type[Any]


class NotifyProvider(ABC):
    @abstractmethod
    async def send(self, **kwargs: dict[str, Any]) -> dict:
        raise NotImplementedError("")

    @abstractmethod
    async def status(self, notify_id: Union[Any, str]) -> Union[Any, Exception]:
        raise NotImplementedError("")

    @abstractmethod
    async def find(self) -> dict[str, Any]:
        raise NotImplementedError("")

    @abstractmethod
    async def find_one(self, sender_id: str) -> dict[str, Any]:
        raise NotImplementedError("")
