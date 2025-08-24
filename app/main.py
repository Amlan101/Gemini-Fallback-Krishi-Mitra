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
        advice = get_gemini_advice(final_prompt)
    except Exception as e:
        # Graceful degradation
        advice = (
            "We faced a temporary issue fetching AI advice. Based on weather forecast, "
            "NDVI, and market data, avoid irrigation before expected rain, monitor leaf color "
            "for stress, and check rising mandi prices before harvest. (Sources: Weather API, Satellite NDVI, Market Prices)"
        )

    return AdviceResponse(
        advice=advice,
        sources=["Weather Forecast API", "Satellite NDVI", "Market Prices"]
    )
