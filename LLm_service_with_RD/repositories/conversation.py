from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from repositories.interface import BaseRepository
from schemas import ConversationCreate, ConversationUpdate
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
    
    async def get(self, conversation_id: int) -> Conversation | None:
        async with self.session.begin():
            result = await self.session.execute(
                self(Conversation).where(Conversation.id == conversation_id)
            )
        return result.scalar_one_or_none()
    
    async def create(self, conversation: ConversationCreate) -> Conversation:
        new_coversation = Conversation(**conversation.model_dump())
        async with self.session.begin():
            self.session.add(new_coversation)
            await self.session.commit()
            await self.session.refresh(new_coversation)
        return new_coversation
    
    async def update(self, conversation_id : int, updated_conversation : Conversation) -> Conversation | None:
        conversation = await self.get(conversation_id)
        if not conversation:
            return None
        for key, value in updated_conversation.model.dump().items():
            setattr(Conversation, key, value)
        async with self.session.begin():
            await self.session.commit()
            await self.session.refresh(conversation)
        return Conversation
    
    async def delete(self,conversation_id : int) -> None:
        conversation = await self.get(conversation_id)
        if not conversation:
            return
        async with self.session.begin():
            await self.session.delete(conversation)
            await self.session.commit()

