from fastapi import FastAPI
from app.models import AdviceRequest, AdviceResponse
from app.prompt_builder import build_prompt
from app.services.gemini_client import get_gemini_advice

app = FastAPI(title="Agri Advice API", version="0.3.0")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/advice", response_model=AdviceResponse)
async def generate_advice(req: AdviceRequest):
    # Stub enrichment data (Phase 4 will fetch real ones)
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

    advice = get_gemini_advice(final_prompt)

    return AdviceResponse(
        advice=advice,
        sources=["Weather Forecast API (stub)", "Satellite NDVI (stub)", "Market Prices (stub)"]
    )
