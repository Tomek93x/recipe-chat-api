from fastapi import APIRouter, Depends, HTTPException

from beanie import PydanticObjectId

from models.user import User
from models.conversation import Conversation
from schemas.chat import ChatMessageRequest, ChatMessageResponse
from services.chat_service import send_chat_message, get_conversation_messages
from core.deps import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/send", response_model=ChatMessageResponse)
async def chat_send(
    payload: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
) -> ChatMessageResponse:
    result = await send_chat_message(
        user_id=str(current_user.id),
        category=payload.category,
        message=payload.message,
        conversation_id=payload.conversation_id,
    )
    return ChatMessageResponse(**result)


@router.get("/{conversation_id}/messages")
async def get_messages(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
):
    # Sprawdz czy konwersacja nalezy do zalogowanego usera
    try:
        conv = await Conversation.get(PydanticObjectId(conversation_id))
    except Exception:
        raise HTTPException(status_code=400, detail="Nieprawidlowe id konwersacji")

    if not conv or conv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Konwersacja nie znaleziona")

    messages = await get_conversation_messages(conversation_id)
    return [
        {
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at.isoformat(),
        }
        for msg in messages
    ]
