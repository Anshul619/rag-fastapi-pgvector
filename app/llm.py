import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-2.0-flash")

def ask_gemini(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns the response text.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error from Gemini: {e}"