from fastapi import FastAPI
from routers.recipe import router as recipe_router

app = FastAPI(title="Recipe Chat API")


@app.get("/")
def read_root():
    return {"message": "Recipe Chat API works"}


app.include_router(recipe_router)