import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ─── FILL THESE IN YOUR .env FILE ───────────────────────────────────────────
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/campus_complaints")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "your-anthropic-api-key-here")
    SECRET_KEY = os.getenv("SECRET_KEY", "campus-agent-secret-key")
    # ────────────────────────────────────────────────────────────────────────────
    DEBUG = os.getenv("DEBUG", "True") == "True"
