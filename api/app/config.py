from dotenv import load_dotenv; load_dotenv()
from pydantic import BaseModel
import os

class Settings(BaseModel):
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("PORT", 8000))
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "*").split(",")

    # Provider keys
    groq_key: str | None = os.getenv("GROQ_API_KEY")
    together_key: str | None = os.getenv("TOGETHER_API_KEY")
    openrouter_key: str | None = os.getenv("OPENROUTER_API_KEY")

    # Scoring models you *have* (from your /models list)
    scoring_models: list[str] = (
        os.getenv("SCORING_MODELS", "llama-3.3-70b-versatile,llama-3.1-8b-instant")
        .split(",")
    )

settings = Settings()
