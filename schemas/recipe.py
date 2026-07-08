from pydantic import BaseModel, Field
from typing import List, Literal

Category = Literal["sniadanie", "obiad", "kolacja"]


class RecipeRequest(BaseModel):
    category: Category
    ingredients: List[str] = Field(min_length=1, max_length=50)


class RecipeResponse(BaseModel):
    recipe_name: str
    category: Category
    ingredients: List[str]
    instructions: str
