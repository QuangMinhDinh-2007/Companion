
CRISIS_KEYWORDS = [
    "kill myself", "end my life", "want to die", "suicide",
    "cut myself", "hurt myself", "self-harm", "no reason to live",
    "can't go on", "better off dead"
]

#TODO: Hotlines pending final verification + counselor review before public launch.
# Sources checked: findahelpline.com/countries/vn (last checked 2026-07-29)
CRISIS_HOTLINES = {
    "national_24_7": "1900 2546",
    "youth": "1800 1567",
    "emergency": "115",
}

CRISIS_RESPONSE = """
    I hear you, and I'm really glad you're talking to me right now.\n"
    "What you're feeling sounds incredibly heavy, and you don't have to carry it alone.\n\n"
    "Please reach out to someone who can be with you right now:\n"
    "• National Suicide Prevention Hotline (24/7): 1900 2546\n"
    "• Blue Dragon youth support (Mon–Fri, 9am–6pm): 1800 1567\n"
    "• If you're in immediate danger, call 115 (emergency).\n\n"
    "I'm still here with you. Can you tell me what's happening right now?"""

def check_for_crisis(message: str) -> bool:
    """Returns True if the message contains crisis signals."""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in CRISIS_KEYWORDS)

def get_crisis_response() -> str:
    """Returns the safe crisis response message."""
    return CRISIS_RESPONSE