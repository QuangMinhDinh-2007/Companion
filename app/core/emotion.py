
import torch
from transformers import pipeline

_emotion_classifier = None

def get_classifier():
    global _emotion_classifier
    if _emotion_classifier is None:
        _emotion_classifier = pipeline(
            "text-classification",
            model="bhadresh-savani/distilbert-base-uncased-emotion",
            top_k=1,
            device=0 if torch.cuda.is_available() else -1,
            truncation=True,
            max_length=512,
        )
    return _emotion_classifier

def detect_emotion(message: str) -> str:
    """Returns the dominant emotion label, e.g. 'sadness', 'joy', 'fear'."""
    try:
        result = get_classifier()(message)
        top = result[0]
        if isinstance(top,list):
            top = top[0]
        return top["label"]
    except Exception:
        return "neutral"