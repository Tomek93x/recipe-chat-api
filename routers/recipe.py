from fastapi import APIRouter
from schemas.recipe import RecipeRequest, RecipeResponse
from services.ollama_service import generate_recipe

router = APIRouter(prefix="/recipe", tags=["recipe"])


@router.post("/generate", response_model=RecipeResponse)
def generate_recipe_endpoint(request: RecipeRequest):
    return generate_recipe(request)