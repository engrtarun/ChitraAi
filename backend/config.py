import os
from dotenv import load_dotenv

# Load from the parent directory since .env is at the root
load_dotenv(dotenv_path="../.env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Puter.js is removed from the backend config.
# Puter.js will be used natively in the Frontend (video-generator-ui)
