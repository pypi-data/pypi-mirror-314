from abc import ABC, abstractmethod


class StorageProvider(ABC):

    @abstractmethod
    async def retrieve_user(self, search_query: dict) -> dict:
        pass

    @abstractmethod
    async def update_user(self, id: str, update_data: dict) -> tuple[int, str | None]:
        pass

    @abstractmethod
    async def insert_user(self, user_data: dict) -> tuple[int, str | None]:
        pass
