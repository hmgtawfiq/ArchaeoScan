def geometry_analysis(data):
    """
    تحليل هندسي أولي لبيانات منطقة البحث.
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

        # حساب التغيرات المحلية في البيانات.
        gradients = np.gradient(array)

        if isinstance(gradients, list):
            magnitude = np.sqrt(
                sum(g ** 2 for g in gradients)
            )
        else:
            magnitude = np.abs(gradients)

        mean_change = float(
            np.nanmean(magnitude)
        )

        score = max(
            0.0,
            min(
                100.0,
                mean_change * 100
            )
        )

        return {
            "score": round(score, 1),
            "status": "ok",
            "mean_change": mean_change
        }

    except Exception as exc:

        return {
            "score": None,
            "status": "error",
            "error": str(exc)
        }
