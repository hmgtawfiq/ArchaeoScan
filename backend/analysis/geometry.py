import math


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

    result = (value - minimum) / (maximum - minimum)

    return max(0.0, min(1.0, result))


def geometry_analysis(
    width,
    height,
    anomaly_pixels,
    total_pixels,
):
    """
    تحليل أولي لشكل وتوزيع البكسلات المرشحة.
    """

    if width <= 0 or height <= 0:
        raise ValueError(
            "Image dimensions must be greater than zero."
        )

    if total_pixels <= 0:
        raise ValueError(
            "Total pixels must be greater than zero."
        )

    anomaly_ratio = anomaly_pixels / total_pixels

    image_area = width * height

    density = anomaly_pixels / image_area

    return {
        "width": width,
        "height": height,
        "anomaly_pixels": anomaly_pixels,
        "total_pixels": total_pixels,
        "anomaly_ratio": anomaly_ratio,
        "density": density,
        "coverage_score": normalize(
            anomaly_ratio,
            0.0,
            1.0,
        ),
    }
