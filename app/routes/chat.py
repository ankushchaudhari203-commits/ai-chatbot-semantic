from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.engine.chatbot_engine import ChatbotEngine
import logging

logger = logging.getLogger("pizza-chatbot")


router = APIRouter(prefix="/chat", tags=["Chat"])

chat_engine = ChatbotEngine()

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply, state = chat_engine.process_message(
        session_id=request.session_id,
        message=request.message
    )

    return ChatResponse(reply=reply, state=state)


