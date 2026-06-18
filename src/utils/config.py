import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "crewai-research-pipeline")
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    KNOWLEDGE_DIR = os.getenv("KNOWLEDGE_DIR", "knowledge")
    STORAGE_DIR = os.getenv("STORAGE_DIR", "storage")

settings = Settings()
