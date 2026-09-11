import numpy as np


def _safe_index(a, b):
    """حساب (A-B)/(A+B) مع تجنب القسمة على صفر."""

    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    denominator = a + b

    return np.divide(
        a - b,
        denominator,
        out=np.zeros_like(
            denominator,
            dtype=float,
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


def create_valid_mask(
    scl,
    data_mask=None,
):
    """
    إنشاء قناع لاستبعاد السحب والبيكسلات
    غير الصالحة من بيانات Sentinel-2.

    قيم SCL المستبعدة:
    0  = No data
    1  = Saturated / defective
    3  = Cloud shadow
    8  = Cloud medium probability
    9  = Cloud high probability
    10 = Thin cirrus
    11 = Snow / ice
    """

    scl = np.asarray(scl)

    invalid_classes = {
        0,
        1,
        3,
        8,
        9,
        10,
        11,
    }

    mask = ~np.isin(
        scl,
        list(invalid_classes),
    )

    if data_mask is not None:
        data_mask = np.asarray(
            data_mask
        )

        mask &= data_mask > 0

    return mask


def apply_mask(values, mask):
    """تطبيق القناع على مصفوفة البيانات."""

    values = np.asarray(
        values,
        dtype=float,
    )

    mask = np.asarray(
        mask,
        dtype=bool,
    )

    return np.where(
        mask,
        values,
        np.nan,
    )


def spectral_analysis(
    blue,
    green,
    red,
    nir,
    swir1,
    swir2,
    scl=None,
    data_mask=None,
):
    """
    حساب المؤشرات الطيفية الأساسية
    مع إمكانية استبعاد السحب والبيكسلات
    غير الصالحة.
    """

    blue = np.asarray(
        blue,
        dtype=float,
    )

    green = np.asarray(
        green,
        dtype=float,
    )

    red = np.asarray(
        red,
        dtype=float,
    )

    nir = np.asarray(
        nir,
        dtype=float,
    )

    swir1 = np.asarray(
        swir1,
        dtype=float,
    )

    swir2 = np.asarray(
        swir2,
        dtype=float,
    )

    if scl is not None:
        mask = create_valid_mask(
            scl,
            data_mask,
        )

        blue = apply_mask(
            blue,
            mask,
        )

        green = apply_mask(
            green,
            mask,
        )

        red = apply_mask(
            red,
            mask,
        )

        nir = apply_mask(
            nir,
            mask,
        )

        swir1 = apply_mask(
            swir1,
            mask,
        )

        swir2 = apply_mask(
            swir2,
            mask,
        )

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
    """تلخيص نتائج المصفوفات إلى قيم مفهومة."""

    summary = {}

    for name, values in results.items():

        array = np.asarray(
            values,
            dtype=float,
        )

        valid = array[
            np.isfinite(array)
        ]

        if valid.size == 0:
            summary[name] = {
                "mean": 0.0,
                "minimum": 0.0,
                "maximum": 0.0,
            }

            continue

        summary[name] = {
            "mean": float(
                np.mean(valid)
            ),
            "minimum": float(
                np.min(valid)
            ),
            "maximum": float(
                np.max(valid)
            ),
        }

    return summary
