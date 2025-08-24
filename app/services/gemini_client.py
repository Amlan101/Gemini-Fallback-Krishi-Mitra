import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, Any

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
        "max_output_tokens": 400,   
        "temperature": 0.3,        
    }
)


def get_gemini_advice(prompt: str) -> Dict[str, Any]:
    """
    Get structured advice from Gemini API.
    Returns a dictionary with title, advice, and sources.
    """
    try:
        response = model.generate_content(prompt)

        # Fallback handling
        if not response or not response.text:
            return {
                "title": "Agricultural Advice",
                "advice": "Unable to generate advice at the moment. Please try again.",
                "sources": ["System Fallback"]
            }

        response_text = response.text.strip()
        
        # Try to parse JSON response
        try:
            # Remove any markdown code block formatting if present
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            parsed_response = json.loads(response_text)
            
            # Validate that all required fields are present
            if all(key in parsed_response for key in ["title", "advice", "sources"]):
                return parsed_response
            else:
                raise ValueError("Missing required fields in response")
                
        except (json.JSONDecodeError, ValueError):
            # If JSON parsing fails, create structured response from plain text
            return {
                "title": "Agricultural Advice",
                "advice": response_text.replace("\n", " ").replace("*", "").strip(),
                "sources": ["Gemini AI", "Agricultural Knowledge Base"]
            }
    
    except Exception as e:
        # Complete fallback in case of any error
        return {
            "title": "Agricultural Advice",
            "advice": "Unable to generate advice at the moment. Please try again later.",
            "sources": ["System Fallback"]
        }
