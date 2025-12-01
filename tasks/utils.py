from datetime import datetime
from django.utils import timezone


def calculate_priority(due_date, estimated_hours, importance, dependencies=None, self_id=None):
    """
    Core scoring function used by both the API and unit tests.
    """
    dependencies = dependencies or []

    # Always work with timezone-aware datetimes
    now = timezone.now()

    if timezone.is_naive(due_date):
        due_date = timezone.make_aware(due_date, timezone.get_current_timezone())

    days_left = (due_date - now).total_seconds() / 86400.0

    # 1) Urgency...
    ...


    # 1) Urgency: closer / overdue = higher
    if days_left <= 0:
        urgency = 10.0
        timing_note = "task is overdue or due now"
    elif days_left < 1:
        urgency = 9.0
        timing_note = f"due very soon (~{days_left:.1f} day)"
    elif days_left < 7:
        urgency = max(5.0, 10.0 - days_left)  # gently decreases within a week
        timing_note = f"due in {days_left:.1f} days"
    else:
        urgency = 3.0
        timing_note = f"due later (~{days_left:.1f} days left)"

    # 2) Importance from user (1–10)
    importance_value = float(importance)

    # 3) Effort bonus: shorter tasks are better (1 / hours)
    if estimated_hours > 0:
        effort_raw = 1.0 / estimated_hours
    else:
        effort_raw = 0.0
    # scale roughly into 0–10
    effort_component = min(effort_raw * 10.0, 10.0)

    # 4) Dependency penalty
    penalty = float(len(dependencies))
    circular = False
    if self_id is not None and self_id in dependencies:
        circular = True
        penalty += 5.0  # extra hit for circular / self dependency

    # Final weighted score
    score = (urgency * 0.4) + (importance_value * 0.4) + (effort_component * 0.2) - penalty

    # Human-readable explanation
    parts = []
    parts.append(f"Urgency {urgency:.1f}/10 because {timing_note}.")
    parts.append(f"Importance contributes {importance_value:.1f}/10 based on your rating.")
    parts.append(
        f"Effort bonus is {effort_component:.1f}/10 "
        f"(estimated {estimated_hours:.2f} hour(s))."
    )

    if dependencies:
        parts.append(
            f"Dependency penalty −{penalty:.1f} because it depends on "
            f"{len(dependencies)} other task(s)."
        )
    else:
        parts.append("No dependencies, so it is easy to start immediately.")

    if circular:
        parts.append("Warning: task is listed as depending on itself (circular dependency).")

    explanation = " ".join(parts)

    return {
        "score": round(score, 3),
        "urgency": round(urgency, 3),
        "effort_component": round(effort_component, 3),
        "penalty": round(penalty, 3),
        "explanation": explanation,
    }


def score_task(task, all_ids=None):
    """
    Backwards-compatible helper in case your views still call score_task(task, all_ids).

    Returns only the numeric score.
    """
    deps = task.get("dependencies") or []
    metrics = calculate_priority(
        due_date=task["due_date"],
        estimated_hours=task["estimated_hours"],
        importance=task["importance"],
        dependencies=deps,
        self_id=task.get("id"),
    )
    return metrics["score"]
