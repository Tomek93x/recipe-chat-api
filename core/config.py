from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Recipe Chat API"
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "recipe_chat_db"
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()