from fastapi import APIRouter, Depends

from models.user import User
from schemas.recipe import RecipeRequest, RecipeResponse
from services.ai_service import generate_recipe
from core.deps import get_current_user

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("/generate", response_model=RecipeResponse)
async def generate(
    payload: RecipeRequest,
    current_user: User = Depends(get_current_user),
) -> RecipeResponse:
    return await generate_recipe(
        category=payload.category,
        ingredients=payload.ingredients,
    )
