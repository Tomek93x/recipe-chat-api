from schemas.recipe import RecipeRequest, RecipeResponse


def generate_recipe(request: RecipeRequest) -> RecipeResponse:
    return RecipeResponse(
        recipe_name="Test recipe",
        category=request.category,
        ingredients=request.ingredients,
        instructions="Mix all ingredients and prepare a simple meal."
    )