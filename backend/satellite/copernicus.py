import math
import requests

from config import (
    CDSE_CLIENT_ID,
    CDSE_CLIENT_SECRET,
    CDSE_TOKEN_URL,
    CDSE_PROCESS_URL,
)


def get_access_token():
    """الحصول على رمز الدخول من Copernicus."""

    if not CDSE_CLIENT_ID or not CDSE_CLIENT_SECRET:
        raise RuntimeError(
            "Copernicus credentials are not configured."
        )

    response = requests.post(
        CDSE_TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": CDSE_CLIENT_ID,
            "client_secret": CDSE_CLIENT_SECRET,
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()["access_token"]


def create_bbox(latitude, longitude, radius_m):
    """إنشاء مربع جغرافي حول الإحداثية."""

    latitude_delta = radius_m / 111320.0

    longitude_delta = radius_m / (
        111320.0
        * max(
            math.cos(math.radians(latitude)),
            0.01,
        )
    )

    return [
        longitude - longitude_delta,
        latitude - latitude_delta,
        longitude + longitude_delta,
        latitude + latitude_delta,
    ]


def get_sentinel_request(
    latitude,
    longitude,
    radius_m,
    start_date,
    end_date,
    max_cloud=20,
):
    """
    تجهيز طلب بيانات Sentinel-2 L2A.
    """

    bbox = create_bbox(
        latitude,
        longitude,
        radius_m,
    )

    return {
        "input": {
            "bounds": {
                "bbox": bbox,
                "properties": {
                    "crs": (
                        "http://www.opengis.net/"
                        "def/crs/OGC/1.3/CRS84"
                    )
                },
            },
            "data": [
                {
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": {
                            "from": (
                                f"{start_date}T00:00:00Z"
                            ),
                            "to": (
                                f"{end_date}T23:59:59Z"
                            ),
                        },
                        "maxCloudCoverage": max_cloud,
                        "mosaickingOrder": "leastCC",
                    },
                }
            ],
        }
    }


def request_sentinel_data(
    latitude,
    longitude,
    radius_m,
    start_date,
    end_date,
    max_cloud=20,
):
    """
    إرسال طلب إلى Copernicus Process API.
    """

    token = get_access_token()

    request_body = get_sentinel_request(
        latitude,
        longitude,
        radius_m,
        start_date,
        end_date,
        max_cloud,
    )

        response = requests.post(
        CDSE_PROCESS_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=request_body,
        timeout=120,
    )

    response.raise_for_status()

    return response
