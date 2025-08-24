def build_prompt(user_prompt: str, category: str, location: str, crop: str,
                 weather: str, ndvi: str, prices: str) -> str:
    """
    Build a structured system prompt for Gemini.
    Ensures we always ask for a structured JSON response with title, advice, and sources.
    """
    return f"""
You are an agricultural advisor for Indian farmers.
The farmer asks: "{user_prompt}"

Farmer context:
- Category: {category}
- Location: {location}
- Crop: {crop}

Relevant data:
- Weather forecast: {weather}
- Satellite NDVI: {ndvi}
- Market prices: {prices}

Instructions:
1. Provide practical, actionable advice for the farmer
2. Use simple, farmer-friendly language in English
3. Consider the weather, crop health (NDVI), and market conditions
4. Respond ONLY in this exact JSON format (no extra text before or after):

{{
  "title": "A short descriptive title (5-8 words max)",
  "advice": "Detailed, practical advice in simple words. Include specific actions the farmer should take based on the context provided.",
  "sources": ["Weather Data", "Satellite Imagery", "Market Intelligence"]
}}

Remember: Output must be valid JSON only. No markdown formatting, no extra text.
"""