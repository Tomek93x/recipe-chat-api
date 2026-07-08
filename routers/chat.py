from fastapi import APIRouter

from schemas.chat import ChatMessageRequest, ChatMessageResponse
from services.chat_service import send_chat_message, get_conversation_messages

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/send", response_model=ChatMessageResponse)
async def chat_send(payload: ChatMessageRequest):
    result = await send_chat_message(
        user_id=payload.user_id,
        category=payload.category,
        message=payload.message,
        conversation_id=payload.conversation_id
    )
    return result


@router.get("/{conversation_id}/messages")
async def get_messages(conversation_id: str):
    messages = await get_conversation_messages(conversation_id)

    return [
        {
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at.isoformat()
        }
        for msg in messages
    ]