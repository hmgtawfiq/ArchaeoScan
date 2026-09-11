import math

import numpy as np


def distance(x1, y1, x2, y2):
    """حساب المسافة بين نقطتين."""
    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


def normalize(value, minimum, maximum):
    """تحويل قيمة إلى نطاق من 0 إلى 1."""

    if maximum <= minimum:
        return 0.0

    result = (
        (value - minimum)
        / (maximum - minimum)
    )

    return max(
        0.0,
        min(1.0, result),
    )


def geometry_analysis(
    width,
    height,
    anomaly_pixels,
    total_pixels,
):
    """
    تحليل مكاني أولي لمنطقة مرشحة.
    """

    if width <= 0 or height <= 0:
        raise ValueError(
            "Image dimensions must be greater than zero."
        )

    if total_pixels <= 0:
        raise ValueError(
            "Total pixels must be greater than zero."
        )

    anomaly_pixels = max(
        0,
        min(anomaly_pixels, total_pixels),
    )

    anomaly_ratio = (
        anomaly_pixels / total_pixels
    )

    image_area = width * height

    density = (
        anomaly_pixels / image_area
    )

    coverage_score = normalize(
        anomaly_ratio,
        0.0,
        1.0,
    )

    return {
        "width": width,
        "height": height,
        "anomaly_pixels": anomaly_pixels,
        "total_pixels": total_pixels,
        "anomaly_ratio": anomaly_ratio,
        "density": density,
        "coverage_score": coverage_score,
    }


def spatial_anomaly_score(
    values,
    threshold=2.0,
):
    """
    حساب درجة أولية للشذوذ المكاني.

    يتم تحديد القيم التي تتجاوز المتوسط
    بعدة انحرافات معيارية.
    """

    array = np.asarray(
        values,
        dtype=float,
    )

    valid = array[
        np.isfinite(array)
    ]

    if valid.size == 0:
        return {
            "score": 0.0,
            "anomaly_pixels": 0,
            "total_pixels": 0,
        }

    mean = float(
        np.mean(valid)
    )

    std = float(
        np.std(valid)
    )

    if std == 0:
        return {
            "score": 0.0,
            "anomaly_pixels": 0,
            "total_pixels": int(
                valid.size
            ),
        }

    anomalies = np.abs(
        array - mean
    ) > (
        threshold * std
    )

    anomaly_pixels = int(
        np.sum(anomalies)
    )

    total_pixels = int(
        valid.size
    )

    ratio = (
        anomaly_pixels
        / total_pixels
    )

    score = normalize(
        ratio,
        0.0,
        0.20,
    ) * 100.0

    return {
        "score": round(
            float(score),
            2,
        ),
        "anomaly_pixels": anomaly_pixels,
        "total_pixels": total_pixels,
        "anomaly_ratio": ratio,
        "mean": mean,
        "std": std,
    }
