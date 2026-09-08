from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from analysis.scoring import (
    calculate_final_score,
    classify_score,
)

app = FastAPI(
    title="ArchaeoScan",
    version="1.0.0",
    description="Remote sensing analysis engine",
)


class AnalysisRequest(BaseModel):
    latitude: float
    longitude: float
    radius_m: float = 500


@app.get("/")
def home():
    return {
        "application": "ArchaeoScan",
        "version": "1.0.0",
        "status": "online",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.post("/api/analyze")
def analyze(request: AnalysisRequest):

    if not -90 <= request.latitude <= 90:
        raise HTTPException(
            status_code=400,
            detail="Invalid latitude",
        )

    if not -180 <= request.longitude <= 180:
        raise HTTPException(
            status_code=400,
            detail="Invalid longitude",
        )

    if request.radius_m <= 0:
        raise HTTPException(
            status_code=400,
            detail="Radius must be positive",
        )

    # المكونات الحقيقية للتحليل ستضاف
    # بعد ربط Sentinel-2 وCopernicus.

    components = []

    final_score = calculate_final_score(
        components
    )

    classification = classify_score(
        final_score
    )

    return {
        "latitude": request.latitude,
        "longitude": request.longitude,
        "radius_m": request.radius_m,
        "score": final_score,
        "classification": classification,
        "status": "ready",
    }
