import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL")
    # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    # LLM_PROVIDER = os.getenv("LLM_PROVIDER", "claude")
    # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"
settings = Settings()