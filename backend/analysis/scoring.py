def clamp_score(value):
    """حصر الدرجة بين 0 و100."""

    return max(
        0.0,
        min(100.0, float(value)),
    )


def calculate_final_score(
    spectral_score,
    temporal_score,
    geometry_score,
):
    """
    حساب الدرجة النهائية من مكونات التحليل.

    الأوزان:
    الطيفي 40%
    الزمني 30%
    المكاني 30%
    """

    spectral_score = clamp_score(
        spectral_score
    )

    temporal_score = clamp_score(
        temporal_score
    )

    geometry_score = clamp_score(
        geometry_score
    )

    final_score = (
        spectral_score * 0.40
        + temporal_score * 0.30
        + geometry_score * 0.30
    )

    return round(
        clamp_score(final_score),
        2,
    )


def score_level(score):
    """تحويل الدرجة إلى مستوى مفهوم."""

    score = clamp_score(score)

    if score < 20:
        return "منخفض جدًا"

    if score < 40:
        return "منخفض"

    if score < 60:
        return "متوسط"

    if score < 80:
        return "مرتفع"

    return "مرتفع جدًا"


def classify_score(score):
    """
    اسم بديل للتصنيف للحفاظ على التوافق
    مع الإصدارات السابقة.
    """

    return score_level(score)


def score_description(score):
    """وصف مختصر للنتيجة."""

    score = clamp_score(score)

    if score < 20:
        return "مؤشرات ضعيفة جدًا ولا تستدعي أولوية للاستكشاف."

    if score < 40:
        return "مؤشرات ضعيفة، مع وجود بعض الاختلافات التي تستحق المراجعة."

    if score < 60:
        return "مؤشرات متوسطة وتحتاج إلى فحص إضافي ومقارنة مع مصادر أخرى."

    if score < 80:
        return "مؤشرات مرتفعة نسبيًا وتستحق أولوية أكبر للفحص الميداني أو التحليل المتقدم."

    return "مؤشرات مرتفعة جدًا وتستحق دراسة متقدمة، ولا تعني بحد ذاتها وجود موقع أثري مؤكد."
