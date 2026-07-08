from pymongo import AsyncMongoClient
from beanie import init_beanie

from core.config import settings
from models.user import User
from models.conversation import Conversation
from models.message import Message


client = AsyncMongoClient(settings.mongo_url)


async def init_db():
    db = client[settings.mongo_db]

    await init_beanie(
        database=db,
        document_models=[User, Conversation, Message]
    )