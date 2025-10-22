from abc import ABC, abstractmethod
from typing import Any

class BaseRepository(ABC):

    @abstractmethod
    async def list(self) -> list[Any]:
        pass

    async def get(self, uid : int) -> Any:
        pass

    async def create(self, record : Any) -> Any:
        pass
    
