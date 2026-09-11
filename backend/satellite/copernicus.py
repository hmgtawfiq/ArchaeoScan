import io
import math

import requests
import rasterio

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
    """تجهيز طلب Sentinel-2 L2A."""

    bbox = create_bbox(
        latitude,
        longitude,
        radius_m,
    )

    evalscript = """
//VERSION=3

function setup() {
    return {
        input: [
            "B02",
            "B03",
            "B04",
            "B08",
            "B11",
            "B12",
            "SCL",
            "dataMask"
        ],
        output: {
            bands: 8,
            sampleType: "FLOAT32"
        }
    };
}

function evaluatePixel(sample) {
    return [
        sample.B02,
        sample.B03,
        sample.B04,
        sample.B08,
        sample.B11,
        sample.B12,
        sample.SCL,
        sample.dataMask
    ];
}
"""

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
                            "maxCloudCoverage": max_cloud,
                        },
                        "mosaickingOrder": "leastCC",
                    },
                }
            ],
        },
        "output": {
            "width": 256,
            "height": 256,
            "responses": [
                {
                    "identifier": "default",
                    "format": {
                        "type": "image/tiff"
                    },
                }
            ],
        },
        "evalscript": evalscript,
    }


def request_sentinel_data(
    latitude,
    longitude,
    radius_m,
    start_date,
    end_date,
    max_cloud=20,
):
    """إرسال طلب حقيقي إلى Copernicus Process API."""

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


def read_sentinel_tiff(response):
    """قراءة TIFF وتحويله إلى مصفوفات رقمية."""

    with rasterio.open(
        io.BytesIO(response.content)
    ) as dataset:

        data = dataset.read()

    return data


def request_two_periods(
    latitude,
    longitude,
    radius_m,
    current_start,
    current_end,
    previous_start,
    previous_end,
    max_cloud=20,
):
    """جلب بيانات Sentinel-2 لفترتين زمنيتين."""

    current_response = request_sentinel_data(
        latitude=latitude,
        longitude=longitude,
        radius_m=radius_m,
        start_date=current_start,
        end_date=current_end,
        max_cloud=max_cloud,
    )

    previous_response = request_sentinel_data(
        latitude=latitude,
        longitude=longitude,
        radius_m=radius_m,
        start_date=previous_start,
        end_date=previous_end,
        max_cloud=max_cloud,
    )

    current_data = read_sentinel_tiff(
        current_response
    )

    previous_data = read_sentinel_tiff(
        previous_response
    )

    return current_data, previous_data
