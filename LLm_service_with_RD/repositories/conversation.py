from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete

from repositories.interface import BaseRepository
from schemas import ConversationCreate, ConversationUpdate,ConversationId
from DB_Model import Conversation

class ConversationRepository(BaseRepository):
    def __init__(self, session : AsyncSession) -> None:
        self.session = session

    async def list(self, skip: int, take : int) -> list[Conversation]:
        async with self.session.begin():
            result = await self.session.execute(
                select(Conversation).offset(skip).limit(take)
            )
            conversation_list = result.scalars().all()
            safe_data = [
            {k: v for k, v in c.__dict__.items() if k != '_sa_instance_state'}
            for c in conversation_list
            ]
        return safe_data
    

    async def get(self, conversation_id: int) -> Conversation | None:
        async with self.session.begin():
            conversation_orm = await self.session.get(Conversation, conversation_id)
            if conversation_orm:
                return ConversationId.model_validate(conversation_orm) 
        return None
    
    async def create(self, conversation: ConversationCreate) -> Conversation:
        new_coversation = Conversation(**conversation.model_dump())
        async with self.session.begin():
            self.session.add(new_coversation)
            await self.session.commit()
        await self.session.refresh(new_coversation)
        return new_coversation
    
    async def update(self, conversation_id : int, updated_conversation : Conversation):
        conversation = await self.get(conversation_id)
        if not conversation:
            return None
        for key, value in updated_conversation.model_dump().items():
            setattr(Conversation, key, value)
        async with self.session.begin():
            await self.session.commit()
        await self.session.refresh(conversation) 
        return Conversation
    
    async def delete(self,conversation_id : int) -> None:
        async with self.session.begin():
            result = await self.session.execute(
                delete(Conversation).where(Conversation.id == conversation_id)
            )
            if result.rowcount == 0:
                return
            await self.session.commit()

