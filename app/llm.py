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

def ask_model(context, question: str) -> str:
    """
    Sends a prompt to Gemini and returns the response text.
    """
    try:
        print(context, question)
        prompt = f"""
        You are a helpful assistant. Use the following context to answer the question.
    
        Context:
        {context}
    
        Question: {question}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error from Gemini: {e}"