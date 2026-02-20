from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.engine.chatbot_engine import ChatbotEngine

router = APIRouter()
chat_engine = ChatbotEngine()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    reply, state, total, items = chat_engine.process_message(
        request.session_id,
        request.message
    )

    return ChatResponse(
        reply=reply,
        state=state,
        total_price=total,
        items=items
    )

