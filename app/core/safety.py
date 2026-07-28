
CRISIS_KEYWORDS = [
    "kill myself", "end my life", "want to die", "suicide",
    "cut myself", "hurt myself", "self-harm", "no reason to live",
    "can't go on", "better off dead"
]

CRISIS_RESPONSE = """
I hear you, and I'm really glad you're talking to me right now.
What you're feeling sounds incredibly heavy.

Please reach out to someone who can be there with you:

I'm still here with you. Can you tell me what's happening right now?
"""

def check_for_crisis(message: str) -> bool:
    """Returns True if the message contains crisis signals."""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in CRISIS_KEYWORDS)

def get_crisis_response() -> str:
    """Returns the safe crisis response message."""
    return CRISIS_RESPONSE