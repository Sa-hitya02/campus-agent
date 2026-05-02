import re
from typing import List, Tuple

# ──────────────────────────────────────────────────────────────────────────────
# Keyword maps for rule-based fallback (used when AI is unavailable)
# ──────────────────────────────────────────────────────────────────────────────

CATEGORY_KEYWORDS = {
    "Infrastructure": [
        "leak", "broken", "repair", "electricity", "power", "water", "toilet",
        "plumbing", "roof", "wall", "floor", "door", "window", "lift", "elevator",
        "building", "construction", "maintenance", "fan", "light", "bulb", "ac",
        "air conditioner", "heating", "pipe", "road", "path", "parking"
    ],
    "Academic": [
        "exam", "grade", "marks", "faculty", "professor", "teacher", "class",
        "course", "curriculum", "syllabus", "lecture", "assignment", "result",
        "timetable", "schedule", "library", "lab", "attendance", "project",
        "internship", "placement", "scholarship", "fee", "admission"
    ],
    "Hostel": [
        "hostel", "room", "roommate", "warden", "food", "mess", "canteen",
        "wifi", "internet", "bed", "mattress", "blanket", "bathroom", "hygiene",
        "laundry", "noise", "curfew", "gate", "security guard"
    ],
    "Safety & Security": [
        "theft", "stolen", "harassment", "ragging", "bully", "threat", "unsafe",
        "danger", "accident", "fire", "cctv", "camera", "crime", "police",
        "violence", "abuse", "eve teasing", "drug", "alcohol"
    ],
    "Administrative": [
        "certificate", "document", "id card", "bonafide", "noc", "migration",
        "transfer", "office", "staff", "administration", "registration",
        "dues", "fine", "penalty", "complaint", "grievance", "portal", "website"
    ],
    "Sports & Facilities": [
        "ground", "gym", "sports", "court", "football", "cricket", "basketball",
        "swimming", "pool", "club", "event", "fest", "cultural", "auditorium",
        "seminar", "workshop", "equipment"
    ],
}

NEGATIVE_WORDS = [
    "terrible", "horrible", "awful", "bad", "poor", "worst", "disgusting",
    "unacceptable", "broken", "failed", "useless", "pathetic", "angry",
    "frustrated", "disappointed", "upset", "annoyed"
]

POSITIVE_WORDS = [
    "good", "great", "excellent", "wonderful", "helpful", "resolved",
    "improved", "better", "satisfied", "happy", "appreciate", "thank"
]


def extract_keywords(text: str) -> List[str]:
    """Extract meaningful keywords from complaint text."""
    text_lower = text.lower()
    words = re.findall(r'\b[a-z]{3,}\b', text_lower)
    stopwords = {
        "the", "and", "for", "that", "this", "with", "have", "from",
        "are", "was", "were", "been", "has", "had", "not", "but", "our",
        "they", "their", "there", "when", "what", "who", "how", "can",
        "could", "would", "should", "will", "its", "also", "very", "please"
    }
    keywords = list(set(w for w in words if w not in stopwords))
    return keywords[:10]


def analyze_sentiment(text: str) -> str:
    """Simple rule-based sentiment analysis."""
    text_lower = text.lower()
    neg = sum(1 for w in NEGATIVE_WORDS if w in text_lower)
    pos = sum(1 for w in POSITIVE_WORDS if w in text_lower)
    if neg > pos:
        return "negative"
    elif pos > neg:
        return "positive"
    return "neutral"


def classify_category_fallback(text: str) -> str:
    """Fallback rule-based category detection."""
    text_lower = text.lower()
    scores = {cat: 0 for cat in CATEGORY_KEYWORDS}
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw in text_lower:
                scores[cat] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "General"
