from fastapi import FastAPI
from app.models import AdviceRequest, AdviceResponse

app = FastAPI(title="Agri Advice API", version="0.1.0")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/advice", response_model=AdviceResponse)
async def generate_advice(req: AdviceRequest):
    """
    Stub endpoint - will later call Gemini with enriched context.
    For now, return dummy advice.
    """
    return AdviceResponse(
        advice=f"Stub advice for {req.crop} in {req.location}.",
        sources=["Stub source"],
    )
