
import anthropic
from .safety import check_for_crisis, get_crisis_response
from .memory import build_context
from .prompts import build_system_prompt
from app.config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def get_response(user_message: str, chat_history: list[dict], emotion: str) -> str:

    if check_for_crisis(user_message):
        return get_crisis_response()

    formatted_history = build_context(chat_history)    
    formatted_history.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=350,
        system=build_system_prompt(emotion or "unknown"),
        messages=formatted_history
    )

    return response.content[0].text