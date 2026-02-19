from enum import Enum

class ConversationState(Enum):
    IDLE = "IDLE"
    ORDERING = "ORDERING"
    CONFIRMING = "CONFIRMING"
    COMPLETED = "COMPLETED"
