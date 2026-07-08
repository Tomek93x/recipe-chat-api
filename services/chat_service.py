from datetime import datetime, timezone
from beanie import PydanticObjectId

from models.conversation import Conversation
from models.message import Message
from services.ai_service import generate_recipe


async def get_or_create_conversation(
    user_id: str, category: str, conversation_id: str | None
) -> Conversation:
    if conversation_id:
        try:
            conversation = await Conversation.get(PydanticObjectId(conversation_id))
        except Exception:
            conversation = None
        if conversation and str(conversation.user_id) == user_id:
            return conversation

    conversation = Conversation(
        user_id=PydanticObjectId(user_id),
        category=category,
        title=f"{category.capitalize()} - czat",
    )
    await conversation.insert()
    return conversation


async def build_prompt(
    conversation_id: PydanticObjectId, category: str, new_message: str
) -> str:
    messages = (
        await Message.find(Message.conversation_id == conversation_id)
        .sort("created_at")
        .to_list()
    )
    history = "\n".join([f"{msg.role}: {msg.content}" for msg in messages])
    return (
        "Jestes pomocnikiem kulinarnym. "
        f"Uzytkownik wybral kategorie posilku: {category}. "
        "Odpowiadaj po polsku. Jesli podano skladniki, zaproponuj konkretne danie, "
        "wymien skladniki (z brakujacymi jesli trzeba) i krotka instrukcje przygotowania.\n\n"
        f"Historia rozmowy:\n{history}\n"
        f"Nowa wiadomosc uzytkownika: {new_message}\n"
        "Twoja odpowiedz:"
    )


async def send_chat_message(
    user_id: str, category: str, message: str, conversation_id: str | None
) -> dict:
    conversation = await get_or_create_conversation(user_id, category, conversation_id)

    # Zapisz wiadomosc usera
    user_msg = Message(
        conversation_id=conversation.id,
        role="user",
        content=message,
    )
    await user_msg.insert()

    # Wygeneruj odpowiedz AI
    prompt = await build_prompt(conversation.id, category, message)
    ai_text = await generate_recipe(prompt=prompt)

    ai_msg = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=ai_text,
    )
    await ai_msg.insert()

    # Aktualizuj updated_at konwersacji
    conversation.updated_at = datetime.now(timezone.utc)
    await conversation.save()

    return {
        "conversation_id": str(conversation.id),
        "user_message": message,
        "ai_message": ai_text,
    }


async def get_conversation_messages(conversation_id: str):
    messages = (
        await Message.find(Message.conversation_id == PydanticObjectId(conversation_id))
        .sort("created_at")
        .to_list()
    )
    return messages