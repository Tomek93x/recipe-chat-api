from beanie import Document, PydanticObjectId
from pydantic import EmailStr, Field
from datetime import datetime, timezone
from typing import Optional

from core.security import hash_password, verify_password


class User(Document):
    email: EmailStr
    username: str
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"

    @classmethod
    async def create(cls, email: str, username: str, password: str) -> "User":
        user = cls(
            email=email,
            username=username,
            hashed_password=hash_password(password),
        )
        await user.insert()
        return user

    async def check_password(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)

    def to_public(self) -> dict:
        return {
            "id": str(self.id),
            "email": self.email,
            "username": self.username,
            "created_at": self.created_at.isoformat(),
        }