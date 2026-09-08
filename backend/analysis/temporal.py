def temporal_analysis(current_data, previous_data):
    """
    مقارنة أولية بين بيانات حالية وبيانات سابقة.
    """

    if current_data is None or previous_data is None:
        return {
            "score": None,
            "status": "no_data"
        }

    try:
        import numpy as np

        current = np.asarray(
            current_data,
            dtype=float
        )

        previous = np.asarray(
            previous_data,
            dtype=float
        )

        if current.size == 0 or previous.size == 0:
            return {
                "score": None,
                "status": "empty_data"
            }

        difference = np.nanmean(
            np.abs(current - previous)
        )

        score = max(
            0.0,
            min(
                100.0,
                float(difference) * 100
            )
        )

        return {
            "score": round(score, 1),
            "status": "ok",
            "change": float(difference)
        }

    except Exception as exc:

        return {
            "score": None,
            "status": "error",
            "error": str(exc)
        }
