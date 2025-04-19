from abc import ABC, abstractmethod
from typing import Any, Type, Union

Class = Type[Any]


class NotifyProvider(ABC):
    @abstractmethod
    async def send(self, model_klass: Class, **kwargs) -> dict:
        """
        Send notification

        :param model_klass:
        :param kwargs:
        :return:
        """
        raise NotImplementedError("")

    @abstractmethod
    async def status(self, notify_id: Union[Any, str]) -> Union[Any, Exception]:
        raise NotImplementedError("")

    @abstractmethod
    async def find(self, query: dict = None, sort: str = None) -> list:
        raise NotImplementedError("")

    @abstractmethod
    async def find_one(self, sender_id: str) -> dict:
        raise NotImplementedError("")
