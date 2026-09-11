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
from analysis.scoring import (
    calculate_final_score,
    score_level,
)
from satellite.copernicus import (
    request_sentinel_data,
    read_sentinel_tiff,
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

    response = request_sentinel_data(
        latitude=request.latitude,
        longitude=request.longitude,
        radius_m=request.radius_m,
        start_date="2026-08-01",
        end_date="2026-09-01",
        max_cloud=20,
    )

    data = read_sentinel_tiff(response)

    if data.shape[0] < 6:
        raise HTTPException(
            status_code=500,
            detail="Insufficient Sentinel-2 bands.",
        )

    blue = data[0]
    green = data[1]
    red = data[2]
    nir = data[3]
    swir1 = data[4]
    swir2 = data[5]

    spectral_results = spectral_analysis(
        blue,
        green,
        red,
        nir,
        swir1,
        swir2,
    )

    spectral_summary = summarize_spectral_results(
        spectral_results
    )

    spatial_result = spatial_anomaly_score(
        spectral_results["ndbi"]
    )

    spectral_score = float(
        np.clip(
            (
                abs(
                    spectral_summary["ndbi"]["mean"]
                ) * 100
            )
            + (
                abs(
                    spectral_summary["ndwi"]["mean"]
                ) * 20
            )
            + (
                abs(
                    spectral_summary["ndvi"]["mean"]
                ) * 10
            ),
            0,
            100,
        )
    )

    temporal_score = 0.0

    geometry_score = spatial_result["score"]

    final_score = calculate_final_score(
        spectral_score,
        temporal_score,
        geometry_score,
    )

    classification = score_level(
        final_score
    )

    return {
        "latitude": request.latitude,
        "longitude": request.longitude,
        "radius_m": request.radius_m,
        "spectral": spectral_summary,
        "spatial": spatial_result,
        "scores": {
            "spectral": round(
                spectral_score,
                2,
            ),
            "temporal": temporal_score,
            "geometry": round(
                geometry_score,
                2,
            ),
            "final": final_score,
        },
        "classification": classification,
        "status": "analysis_complete",
    }
