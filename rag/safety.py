# rag/safety.py

import re

# ⚠️ High-risk keywords for elders
RISK_KEYWORDS = [
    "suicide", "die", "kill myself", "end my life",
    "chest pain", "heart attack", "unconscious",
    "bleeding", "stroke", "breathless",
    "overdose", "poison"
]

def detect_risk(text: str) -> bool:
    text = text.lower()
    for word in RISK_KEYWORDS:
        if re.search(word, text):
            return True
    return False


def emergency_message():
    return (
        "⚠️ This sounds serious.\n\n"
        "Please seek immediate help:\n"
        "• Call a nearby family member\n"
        "• Visit the nearest hospital\n"
        "• In India: Dial 112 for emergency services\n\n"
        "I am here to support you, but a doctor or caregiver must help now."
    )


def safety_filter(response: str) -> str:
    """
    Ensures elder-friendly tone:
    - No fear
    - No medical commands
    - Simple language
    """
    forbidden_phrases = ["you must", "immediately do", "fatal", "dangerous"]
    for phrase in forbidden_phrases:
        response = response.replace(phrase, "")

    return response
