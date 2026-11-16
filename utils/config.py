import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

APP_NAME = os.getenv("APP_NAME","ASK YOUR DOC")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL","all-MiniLM-L6-v2")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE",1000))

CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP",1000))

TOP_K = int(os.getenv("TOP_K",3))

if not GEMINI_API_KEY:
    raise ValueError("Gemini API Key is missing!")

