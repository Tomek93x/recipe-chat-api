from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from beanie import PydanticObjectId

from core.security import decode_access_token
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidlowy lub wygasniety token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await User.get(PydanticObjectId(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="Uzytkownik nie istnieje")
    return user
