from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Course Inference Service")


class PredictRequest(BaseModel):
    x1: float = Field(..., description="Feature 1")
    x2: float = Field(..., description="Feature 2")


class PredictResponse(BaseModel):
    score: float
    label: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    score = 0.7 * req.x1 + 0.3 * req.x2
    label = int(score >= 0.5)
    return PredictResponse(score=score, label=label)
