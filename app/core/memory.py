
MAX_MESSAGES = 20        
CHARS_PER_TOKEN = 4      
MAX_CONTEXT_TOKENS = 4000


def build_context(chat_history: list[dict]) -> list[dict]:
    
    recent = chat_history[-MAX_MESSAGES:]

    trimmed = []
    total_chars = 0
    budget = MAX_CONTEXT_TOKENS * CHARS_PER_TOKEN

    for msg in reversed(recent):          # newest first while counting
        total_chars += len(msg["content"])
        if total_chars > budget:
            break
        trimmed.append(msg)

    return list(reversed(trimmed))        # back to chronological order