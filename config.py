import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

MODEL_NAME = "gemini-1.5-pro"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "Image", "Logo.png")
INVERSE_LOGO_PATH = os.path.join(BASE_DIR, "Image", "inverseLogo.png")