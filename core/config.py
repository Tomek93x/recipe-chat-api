from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Recipe Chat API"

    # MongoDB
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "recipe_chat_db"

    secret_key: str = "change-me-in-env"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    # AI provider: "ollama", "openai" albo "gemini"
    ai_provider: str = "ollama"

    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()