
from .supabase import get_db

def save_message(user_id: str, role: str, content: str, emotion: str = None):
    """Saves one message (either from the user or the AI) to the database."""
    get_db().table("conversations").insert({
        "user_id": user_id,
        "role": role,
        "content": content,
        "emotion": emotion
    }).execute()

def get_history(user_id: str, limit: int = 20) -> list[dict]:
    """Fetches the last N messages for a user, oldest first."""
    result = (
        get_db().table("conversations")
        .select("role, content")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
        .select("role, content, emotion")
    )
    return list(reversed(result.data))