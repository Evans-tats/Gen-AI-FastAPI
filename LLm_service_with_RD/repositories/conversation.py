from repositories.interface import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from DB_Model import Conversation

class ConversationRepository(BaseRepository):
    def __init__(self, session : AsyncSession) -> None:
        self.session = session

    async def list(self, skip: int, take : int) -> list[Conversation]:
        async with self.session.begin():
            result = await self.session.execute(
                select(Conversation).offset(skip).limit(take)
            )
        return [r for r in result.scalars().all()]