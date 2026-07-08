from fastapi import APIRouter

from models.conversation import Conversation

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get("/{user_id}")
async def get_user_conversations(user_id: str):
    conversations = await Conversation.find({"user_id": user_id}).sort("-created_at").to_list()
    return conversations