def calculate_final_score(components):
    """
    حساب النتيجة النهائية من مكونات التحليل المتوفرة.
    """

    available = [
        component
        for component in components
        if component.get("score") is not None
    ]

    if not available:
        return 0.0

    total_weight = sum(
        component.get("weight", 0)
        for component in available
    )

    if total_weight <= 0:
        return 0.0

    weighted_score = sum(
        component["score"]
        * component.get("weight", 0)
        for component in available
    )

    return round(
        weighted_score / total_weight,
        1
    )


def classify_score(score):
    """
    تحويل الدرجة الرقمية إلى تصنيف مبسط.
    """

    if score < 25:
        return "منخفض جداً"

    if score < 50:
        return "منخفض"

    if score < 70:
        return "متوسط"

    if score < 85:
        return "مرتفع"

    return "مرتفع جداً"
