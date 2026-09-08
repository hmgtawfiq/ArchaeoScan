def spectral_analysis(data):
    """
    تحليل طيفي أولي لبيانات الاستشعار عن بعد.

    data:
        مصفوفة NumPy أو بيانات تحتوي على النطاقات الطيفية.
    """

    if data is None:
        return {
            "score": None,
            "status": "no_data"
        }

    try:
        import numpy as np

        array = np.asarray(data, dtype=float)

        if array.size == 0:
            return {
                "score": None,
                "status": "empty_data"
            }

        # حساب متوسط القيم كخطوة أولية.
        mean_value = float(np.nanmean(array))

        # تحويل القيمة إلى مؤشر بين 0 و100.
        score = max(
            0.0,
            min(
                100.0,
                abs(mean_value) * 100
            )
        )

        return {
            "score": round(score, 1),
            "status": "ok",
            "mean_value": mean_value
        }

    except Exception as exc:

        return {
            "score": None,
            "status": "error",
            "error": str(exc)
        }
