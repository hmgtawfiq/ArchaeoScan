def _safe_index(a, b):
    """حساب مؤشر (A-B)/(A+B) مع تجنب القسمة على صفر."""
    denominator = a + b

    if denominator == 0:
        return 0.0

    return (a - b) / denominator


def ndvi(red, nir):
    """Normalized Difference Vegetation Index."""
    return _safe_index(nir, red)


def ndwi(green, nir):
    """Normalized Difference Water Index."""
    return _safe_index(green, nir)


def ndbi(swir, nir):
    """Normalized Difference Built-up Index."""
    return _safe_index(swir, nir)


def spectral_analysis(
    blue,
    green,
    red,
    nir,
    swir1,
    swir2,
):
    """
    حساب مجموعة من المؤشرات الطيفية الأساسية
    من نطاقات Sentinel-2.
    """

    return {
        "ndvi": ndvi(red, nir),
        "ndwi": ndwi(green, nir),
        "ndbi": ndbi(swir1, nir),
        "brightness": (
            blue + green + red + nir + swir1 + swir2
        ) / 6.0,
    }
