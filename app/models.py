from pydantic import BaseModel
from typing import List

class AdviceRequest(BaseModel):
    prompt: str
    category: str
    location: str
    crop: str

class AdviceResponse(BaseModel):
    title: str
    advice: str
    sources: List[str]