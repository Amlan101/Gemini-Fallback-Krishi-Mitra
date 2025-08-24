from fastapi import FastAPI
from app.models import AdviceRequest, AdviceResponse
from app.prompt_builder import build_prompt
from app.services.gemini_client import get_gemini_advice

app = FastAPI(title="Agri Advice API", version="0.3.0")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/fallback_advice", response_model=AdviceResponse)
async def generate_advice(req: AdviceRequest):
    weather_summary = "Light rain expected in 2 days, avg temp 30°C"
    ndvi_summary = "NDVI indicates healthy crop growth"
    price_summary = "Market price for wheat is rising in local mandi"

    final_prompt = build_prompt(
        user_prompt=req.prompt,
        category=req.category,
        location=req.location,
        crop=req.crop,
        weather=weather_summary,
        ndvi=ndvi_summary,
        prices=price_summary
    )

    try:
        gemini_response = get_gemini_advice(final_prompt)
        
        return AdviceResponse(
            title=gemini_response["title"],
            advice=gemini_response["advice"],
            sources=gemini_response["sources"]
        )
    except Exception as e:
        # Fallback response with structured data
        return AdviceResponse(
            title="Agricultural Guidance",
            advice=(
                "We faced a temporary issue fetching AI advice. Based on weather forecast, "
                "NDVI, and market data, avoid irrigation before expected rain, monitor leaf color "
                "for stress, and check rising mandi prices before harvest."
            ),
            sources=["Weather Forecast API", "Satellite NDVI", "Market Prices"]
        )
