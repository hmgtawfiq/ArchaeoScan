def clamp(value, minimum=0.0, maximum=100.0):
    """حصر القيمة ضمن نطاق محدد."""
    return max(minimum, min(maximum, value))


def calculate_final_score(
    spectral_score,
    temporal_score,
    geometry_score,
):
    """
    حساب الدرجة النهائية من نتائج التحليلات.

    الأوزان:
    40% طيفي
    30% زمني
    30% هندسي
    """

    score = (
        spectral_score * 0.40
        + temporal_score * 0.30
        + geometry_score * 0.30
    )

    return round(clamp(score), 2)


def score_level(score):
    """تحويل الدرجة إلى مستوى مبسط."""

    score = clamp(score)

    if score < 30:
        return "منخفض"

    if score < 60:
        return "متوسط"

    if score < 80:
        return "مرتفع"

    return "مرتفع جدًا"
