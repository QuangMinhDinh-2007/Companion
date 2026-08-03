from fastapi import APIRouter, Depends
from app.models.chat_schema import ChatRequest, ChatResponse
from app.core.companion import get_response
from app.core.emotion import detect_emotion
from app.core.auth import get_current_user_id
from app.db.conversations import save_message, get_history
from app.core.safety import check_for_crisis, get_crisis_response

router = APIRouter()

@router.post("/chat", response_model = ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id)
) :
    #Check crisis
    if check_for_crisis(request.message):
        reply = get_crisis_response()
        save_message(user_id, "user", request.message, "crisis")
        save_message(user_id, "assistant", reply)
        return ChatResponse(reply=reply, emotion="crisis")
    
    history = get_history(user_id)
    emotion = detect_emotion(request.message)
    reply = get_response(request.message, history, emotion)
    save_message(user_id, "user", request.message, emotion)
    save_message(user_id, "assistant", reply)

    return ChatResponse(reply = reply, emotion = emotion)
