import numpy as np


def temporal_difference(current, previous):
    """حساب الفرق بين القياس الحالي والسابق."""
    return np.asarray(current, dtype=float) - np.asarray(
        previous, dtype=float
    )


def temporal_change(current, previous):
    """حساب نسبة التغير بين قياسين."""

    current = np.asarray(current, dtype=float)
    previous = np.asarray(previous, dtype=float)

    denominator = np.abs(previous)

    return np.divide(
        current - previous,
        denominator,
        out=np.zeros_like(current, dtype=float),
        where=denominator != 0,
    )


def temporal_analysis(
    current_values,
    previous_values,
):
    """
    تحليل التغير الزمني بين مجموعتين من بيانات Sentinel-2.
    """

    current = np.asarray(
        current_values,
        dtype=float,
    )

    previous = np.asarray(
        previous_values,
        dtype=float,
    )

    if current.shape != previous.shape:
        raise ValueError(
            "Current and previous datasets must have the same shape."
        )

    difference = temporal_difference(
        current,
        previous,
    )

    change = temporal_change(
        current,
        previous,
    )

    valid_difference = difference[
        np.isfinite(difference)
    ]

    valid_change = change[
        np.isfinite(change)
    ]

    if valid_difference.size == 0:
        mean_difference = 0.0
    else:
        mean_difference = float(
            np.mean(valid_difference)
        )

    if valid_change.size == 0:
        mean_change = 0.0
    else:
        mean_change = float(
            np.mean(valid_change)
        )

    return {
        "mean_difference": mean_difference,
        "mean_change": mean_change,
        "difference": difference,
        "change": change,
    }


def temporal_anomaly_score(
    current_values,
    previous_values,
):
    """
    حساب درجة أولية للتغير الزمني.

    هذه الدرجة مؤشر للاستكشاف وليست
    دليلًا على وجود أثر.
    """

    result = temporal_analysis(
        current_values,
        previous_values,
    )

    change = np.asarray(
        result["change"],
        dtype=float,
    )

    valid = change[
        np.isfinite(change)
    ]

    if valid.size == 0:
        return {
            "score": 0.0,
            "mean_change": 0.0,
            "changed_pixels": 0,
            "total_pixels": 0,
        }

    threshold = 0.20

    changed = np.abs(valid) > threshold

    changed_pixels = int(
        np.sum(changed)
    )

    total_pixels = int(
        valid.size
    )

    ratio = (
        changed_pixels
        / total_pixels
    )

    score = min(
        100.0,
        ratio / 0.20 * 100.0,
    )

    return {
        "score": round(
            float(score),
            2,
        ),
        "mean_change": float(
            np.mean(valid)
        ),
        "changed_pixels": changed_pixels,
        "total_pixels": total_pixels,
        "change_ratio": float(ratio),
    }
