def temporal_difference(current, previous):
    """حساب الفرق بين القياس الحالي والسابق."""
    return current - previous


def temporal_change(current, previous):
    """حساب نسبة التغير بين قياسين."""
    if previous == 0:
        return 0.0

    return (current - previous) / abs(previous)


def temporal_analysis(
    current_values,
    previous_values,
):
    """
    تحليل التغير الزمني بين مجموعتين من القيم.
    """

    if len(current_values) != len(previous_values):
        raise ValueError(
            "Current and previous datasets must have the same length."
        )

    differences = [
        temporal_difference(current, previous)
        for current, previous
        in zip(current_values, previous_values)
    ]

    changes = [
        temporal_change(current, previous)
        for current, previous
        in zip(current_values, previous_values)
    ]

    return {
        "differences": differences,
        "changes": changes,
        "mean_difference": (
            sum(differences) / len(differences)
            if differences
            else 0.0
        ),
        "mean_change": (
            sum(changes) / len(changes)
            if changes
            else 0.0
        ),
    }
