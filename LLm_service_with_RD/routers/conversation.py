from typing import Annotated
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status

from repositories.conversation import ConversationRepository
from database_connection import DBSessionDep
from DB_Model import Conversation, Message
from schemas import ConversationOut, ConversationCreate, ConversationId
from services.conversation import ConversationaService

router = APIRouter(prefix="/conversation")

async def get_conversation(conversation_id : int, session : DBSessionDep) -> Conversation:
    conversation = await ConversationRepository(session).get(conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="conversation not found"
        )
    return conversation
    return ConversationOut.model_validate(conversation)

GetConversationDep = Annotated[Conversation, Depends(get_conversation)]

@router.get("")
async def list_conversation_controller(session : DBSessionDep, skip : int = 0, take : int =100):
    conversation_list = await ConversationRepository(session).list(skip, take)
    return [ConversationOut.model_validate(c) for c in conversation_list]

@router.post("")
async def create_conversation_controller(session : DBSessionDep, conversation : ConversationCreate):
    new_conversation = await ConversationRepository(session).create(conversation)
    return ConversationOut.model_validate(new_conversation)

@router.put("/{id}")
async def update_conversation_controller(updated_conversation: ConversationCreate,conversation : GetConversationDep, session : DBSessionDep):
    updated_conversation = await ConversationRepository(session).update(
        conversation.id, updated_conversation
    )
    return ConversationOut.model_validate(updated_conversation)

@router.delete("/{id}")
async def delete_conversation_controller(conversation: GetConversationDep, session:DBSessionDep):
    await ConversationRepository(session).delete(conversation.id)

@router.get("/{conversation_id}/messages")
async def list_conversation_messages_controller(conversation_id: int, session : DBSessionDep):
    messages_Out = ConversationaService(session).list_messages(conversation_id)
    return [m for m in messages_Out]