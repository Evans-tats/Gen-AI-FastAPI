from DB_Model import Message
from sqlalchemy import select
from repositories.conversation import ConversationRepository

class ConversationaService(ConversationRepository):
    async def list_messages(self, conversation_id: int) -> list[Message]:
        result = await self.session.execute(
            select(Message).where(Message.conversation_id == conversation_id)
        )