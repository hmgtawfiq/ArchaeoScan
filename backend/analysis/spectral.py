def _safe_index(a, b):
    """حساب (A-B)/(A+B) مع تجنب القسمة على صفر."""
    denominator = a + b

    if denominator == 0:
        return 0.0

    return (a - b) / denominator


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
    من نطاقات Sentinel-2.
    """

    values = {
        "ndvi": ndvi(red, nir),
        "ndwi": ndwi(green, nir),
        "ndbi": ndbi(swir1, nir),
        "brightness": (
            blue + green + red + nir + swir1 + swir2
        ) / 6.0,
    }

    return values
