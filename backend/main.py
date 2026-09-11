import numpy as np

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from analysis.spectral import (
    spectral_analysis,
    summarize_spectral_results,
)
from analysis.geometry import (
    spatial_anomaly_score,
)
from analysis.temporal import (
    temporal_anomaly_score,
)
from analysis.scoring import (
    calculate_final_score,
    score_level,
    score_description,
)
from satellite.copernicus import (
    request_two_periods,
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

    current_data, previous_data = request_two_periods(
        latitude=request.latitude,
        longitude=request.longitude,
        radius_m=request.radius_m,
        current_start="2026-08-01",
        current_end="2026-09-01",
        previous_start="2026-07-01",
        previous_end="2026-07-31",
        max_cloud=20,
    )

    if current_data.shape[0] < 8:
        raise HTTPException(
            status_code=500,
            detail="Insufficient current Sentinel-2 bands.",
        )

    if previous_data.shape[0] < 8:
        raise HTTPException(
            status_code=500,
            detail="Insufficient previous Sentinel-2 bands.",
        )

    current_spectral = spectral_analysis(
        current_data[0],
        current_data[1],
        current_data[2],
        current_data[3],
        current_data[4],
        current_data[5],
        current_data[6],
        current_data[7],
    )

    previous_spectral = spectral_analysis(
        previous_data[0],
        previous_data[1],
        previous_data[2],
        previous_data[3],
        previous_data[4],
        previous_data[5],
        previous_data[6],
        previous_data[7],
    )

    current_summary = summarize_spectral_results(
        current_spectral
    )

    previous_summary = summarize_spectral_results(
        previous_spectral
    )

    spatial_result = spatial_anomaly_score(
        current_spectral["ndbi"]
    )

    temporal_result = temporal_anomaly_score(
        current_spectral["ndbi"],
        previous_spectral["ndbi"],
    )

    spectral_score = float(
        np.clip(
            (
                abs(
                    current_summary["ndbi"]["mean"]
                ) * 100
            )
            + (
                abs(
                    current_summary["ndwi"]["mean"]
                ) * 20
            )
            + (
                abs(
                    current_summary["ndvi"]["mean"]
                ) * 10
            ),
            0,
            100,
        )
    )

    temporal_score = temporal_result["score"]

    geometry_score = spatial_result["score"]

    final_score = calculate_final_score(
        spectral_score,
        temporal_score,
        geometry_score,
    )

    classification = score_level(
        final_score
    )

    description = score_description(
        final_score
    )

    return {
        "latitude": request.latitude,
        "longitude": request.longitude,
        "radius_m": request.radius_m,
        "current": current_summary,
        "previous": previous_summary,
        "spatial": spatial_result,
        "temporal": temporal_result,
        "scores": {
            "spectral": round(
                spectral_score,
                2,
            ),
            "temporal": round(
                temporal_score,
                2,
            ),
            "geometry": round(
                geometry_score,
                2,
            ),
            "final": final_score,
        },
        "classification": classification,
        "description": description,
        "status": "analysis_complete",
    }
