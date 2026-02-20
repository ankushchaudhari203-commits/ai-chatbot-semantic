from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    state: str

class ChatResponse(BaseModel):
    reply: str
    state: str
    total_price: Optional[float] = None
    items: Optional[List[str]] = None
