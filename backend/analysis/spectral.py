import numpy as np


def _safe_index(a, b):
    """حساب (A-B)/(A+B) مع تجنب القسمة على صفر."""

    denominator = a + b

    return np.divide(
        a - b,
        denominator,
        out=np.zeros_like(
            np.asarray(a, dtype=float)
        ),
        where=denominator != 0,
    )


def ndvi(red, nir):
    """مؤشر الغطاء النباتي NDVI."""
    return _safe_index(nir, red)


def ndwi(green, nir):
    """مؤشر المياه NDWI."""
    return _safe_index(green, nir)


def ndbi(swir1, nir):
    """مؤشر المناطق المبنية NDBI."""
    return _safe_index(swir1, nir)


def spectral_analysis(
    blue,
    green,
    red,
    nir,
    swir1,
    swir2,
):
    """
    حساب المؤشرات الطيفية الأساسية
    من بيانات Sentinel-2.

    يمكن أن تكون المدخلات قيماً مفردة
    أو مصفوفات NumPy.
    """

    blue = np.asarray(blue, dtype=float)
    green = np.asarray(green, dtype=float)
    red = np.asarray(red, dtype=float)
    nir = np.asarray(nir, dtype=float)
    swir1 = np.asarray(swir1, dtype=float)
    swir2 = np.asarray(swir2, dtype=float)

    return {
        "ndvi": ndvi(red, nir),
        "ndwi": ndwi(green, nir),
        "ndbi": ndbi(swir1, nir),
        "brightness": (
            blue
            + green
            + red
            + nir
            + swir1
            + swir2
        ) / 6.0,
    }


def summarize_spectral_results(results):
    """
    تلخيص نتائج المصفوفات إلى قيم مفهومة.
    """

    summary = {}

    for name, values in results.items():
        array = np.asarray(values, dtype=float)

        valid = array[np.isfinite(array)]

        if valid.size == 0:
            summary[name] = {
                "mean": 0.0,
                "minimum": 0.0,
                "maximum": 0.0,
            }
            continue

        summary[name] = {
            "mean": float(np.mean(valid)),
            "minimum": float(np.min(valid)),
            "maximum": float(np.max(valid)),
        }

    return summary
