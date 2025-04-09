import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_KEY")
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")

