from pydantic import BaseModel
from typing import List


class RecipeRequest(BaseModel):
    category: str
    ingredients: List[str]


class RecipeResponse(BaseModel):
    recipe_name: str
    category: str
    ingredients: List[str]
    instructions: str