from beanie import Document
from pydantic import EmailStr
from datetime import datetime, timezone


class User(Document):
    email: EmailStr
    username: str
    hashed_password: str
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "users"