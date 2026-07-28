
from transformers import pipeline

_emotion_classifier = None

def get_classifier():
    global _emotion_classifier
    if _emotion_classifier is None:
        _emotion_classifier = pipeline(
            "text-classification",
            model="bhadresh-savani/distilbert-base-uncased-emotion",
            top_k=1
        )
    return _emotion_classifier

def detect_emotion(message: str) -> str:
    """Returns the dominant emotion label, e.g. 'sadness', 'joy', 'fear'."""
    try:
        classifier = get_classifier()
        result = classifier(message)
        return result[0][0]["label"]
    except Exception:
        return "neutral"