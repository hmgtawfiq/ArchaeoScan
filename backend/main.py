from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from analysis.scoring import (
    calculate_final_score,
    score_level,
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

    # درجات مؤقتة إلى أن يتم ربط التحليل
    # الفعلي ببيانات Sentinel-2.
    spectral_score = 0.0
    temporal_score = 0.0
    geometry_score = 0.0

    final_score = calculate_final_score(
        spectral_score,
        temporal_score,
        geometry_score,
    )

    classification = score_level(final_score)

    return {
        "latitude": request.latitude,
        "longitude": request.longitude,
        "radius_m": request.radius_m,
        "score": final_score,
        "classification": classification,
        "status": "ready",
    }
