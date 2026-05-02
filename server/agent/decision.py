from typing import Tuple

# ──────────────────────────────────────────────────────────────────────────────
# Department mapping per category
# ──────────────────────────────────────────────────────────────────────────────

DEPARTMENT_MAP = {
    "Infrastructure":       "Facilities & Maintenance Department",
    "Academic":             "Academic Affairs Office",
    "Hostel":               "Hostel Administration Office",
    "Safety & Security":    "Campus Security & Student Welfare Cell",
    "Administrative":       "Administrative Services Office",
    "Sports & Facilities":  "Sports & Student Activities Department",
    "General":              "Student Grievance Cell",
}

# ──────────────────────────────────────────────────────────────────────────────
# Priority keywords
# ──────────────────────────────────────────────────────────────────────────────

HIGH_PRIORITY_SIGNALS = [
    "urgent", "emergency", "immediately", "asap", "critical", "danger",
    "unsafe", "harassment", "ragging", "fire", "accident", "violence",
    "threat", "broken since", "days", "weeks", "no water", "no power",
    "not working for", "still not fixed"
]

MEDIUM_PRIORITY_SIGNALS = [
    "not working", "issue", "problem", "concern", "broken", "poor",
    "request", "need", "require", "fix", "repair", "slow", "delayed"
]


def assign_priority(text: str, category: str) -> str:
    """
    Returns: 'High' | 'Medium' | 'Low'
    Safety issues are always High.
    """
    if category == "Safety & Security":
        return "High"

    text_lower = text.lower()

    for signal in HIGH_PRIORITY_SIGNALS:
        if signal in text_lower:
            return "High"

    for signal in MEDIUM_PRIORITY_SIGNALS:
        if signal in text_lower:
            return "Medium"

    return "Low"


def assign_department(category: str) -> str:
    """Map complaint category to responsible department."""
    return DEPARTMENT_MAP.get(category, DEPARTMENT_MAP["General"])


def decide(category: str, text: str) -> Tuple[str, str]:
    """
    Main decision function.
    Returns: (priority, department)
    """
    priority = assign_priority(text, category)
    department = assign_department(category)
    return priority, department
