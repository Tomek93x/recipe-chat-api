from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.user import User
from schemas.auth import RegisterRequest, TokenResponse, UserPublic
from core.security import create_access_token
from core.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=201)
async def register(payload: RegisterRequest) -> UserPublic:
    # Sprawdz czy email/username sa juz zajete
    if await User.find_one(User.email == payload.email):
        raise HTTPException(status_code=400, detail="Email jest juz zajety")
    if await User.find_one(User.username == payload.username):
        raise HTTPException(status_code=400, detail="Nazwa uzytkownika jest zajeta")

    user = await User.create(
        email=payload.email,
        username=payload.username,
        password=payload.password,
    )
    return UserPublic(**user.to_public())


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    user = await User.find_one(User.username == form_data.username)
    if not user or not await user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidlowa nazwa uzytkownika lub haslo",
        )
    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserPublic)
async def me(current_user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic(**current_user.to_public())
