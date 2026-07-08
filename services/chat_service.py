from beanie import PydanticObjectId

from models.conversation import Conversation
from models.message import Message
from services.ollama_service import generate_recipe_response


async def get_or_create_conversation(user_id: str, category: str, conversation_id: str | None):
    if conversation_id:
        conversation = await Conversation.get(PydanticObjectId(conversation_id))
        if conversation:
            return conversation

    conversation = Conversation(
        user_id=PydanticObjectId(user_id),
        category=category,
        title=f"{category.capitalize()} chat"
    )
    await conversation.insert()
    return conversation


async def build_prompt(conversation_id: PydanticObjectId, category: str, new_message: str) -> str:
    messages = await Message.find(Message.conversation_id == conversation_id).sort("created_at").to_list()

    history = "\n".join([f"{msg.role}: {msg.content}" for msg in messages])

    return (
        f"Jesteś pomocnikiem kulinarnym.\n"
        f"Kategoria posiłku: {category}\n"
        f"Historia rozmowy:\n{history}\n"
        f"Nowa wiadomość użytkownika: {new_message}\n"
        f"Odpowiedz po polsku i zaproponuj danie lub przepis na podstawie składników."
    )


async def send_chat_message(user_id: str, category: str, message: str, conversation_id: str | None):
    conversation = await get_or_create_conversation(user_id, category, conversation_id)

    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=message
    )
    await user_message.insert()

    prompt = await build_prompt(conversation.id, category, message)
    ai_text = await generate_recipe_response(prompt)

    ai_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=ai_text
    )
    await ai_message.insert()

    return {
        "conversation_id": str(conversation.id),
        "user_message": message,
        "ai_message": ai_text
    }


async def get_conversation_messages(conversation_id: str):
    messages = await Message.find(
        Message.conversation_id == PydanticObjectId(conversation_id)
    ).sort("created_at").to_list()

    return messages