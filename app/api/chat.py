from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.core.companion import get_response
from app.core.emotion import detect_emotion
from app.db.conversations import save_message, get_history
from app.core.safety import check_for_crisis, get_crisis_response

router = APIRouter()

@router.post("/chat", response_model = ChatResponse)
async def chat(request: ChatRequest) :
    #Check crisis
    if check_for_crisis(request.message):
        reply = get_crisis_response()
        save_message(request.user_id, "user", request.message, "crisis")
        save_message(request.user_id, "assistant", reply)
        return ChatResponse(reply=reply, emotion="crisis")
    
    history = get_history(request.user_id)
    emotion = detect_emotion(request.message)
    reply = get_response(request.message, history, emotion)
    save_message(request.user_id, "user", request.message, emotion)
    save_message(request.user_id, "assistant", reply)

    return ChatResponse(reply = reply, emotion = emotion)
