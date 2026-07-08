from fastapi import APIRouter, Depends
from beanie import PydanticObjectId

from models.user import User
from models.conversation import Conversation
from core.deps import get_current_user

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get("/")
async def list_my_conversations(
    current_user: User = Depends(get_current_user),
):
    conversations = (
        await Conversation.find(Conversation.user_id == current_user.id)
        .sort("-updated_at")
        .to_list()
    )
    return [
        {
            "id": str(c.id),
            "category": c.category,
            "title": c.title,
            "created_at": c.created_at.isoformat(),
            "updated_at": c.updated_at.isoformat(),
        }
        for c in conversations
    ]
