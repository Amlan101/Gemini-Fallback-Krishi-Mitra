import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found. Please set it in your .env file.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Create a reusable model instance
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    generation_config={
        "max_output_tokens": 200,   
        "temperature": 0.3,        
    }
)


def get_gemini_advice(prompt: str) -> str:
    """
    Send a prompt to Gemini and return a clean string response.
    Ensures the response is a single line of advice.
    """
    response = model.generate_content(prompt)

    # Fallback handling
    if not response or not response.text:
        return "Unable to generate advice at the moment. Please try again."

    advice = response.text.strip()

    # Post-process: force plain string, no markdown/bullets
    advice = advice.replace("\n", " ").replace("*", "").strip()

    return advice
