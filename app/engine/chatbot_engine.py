from app.engine.intent_matcher import IntentMatcher
import os
import json
from app.engine.conversation_engine import ConversationEngine
from app.engine.intent_matcher import IntentMatcher


class ChatbotEngine:

    def __init__(self):
        self.sessions = {}

        # Load responses.json
        base_dir = os.path.dirname(os.path.dirname(__file__))
        data_path = os.path.join(base_dir, "data", "responses.json")

        with open(data_path, "r") as f:
            responses = json.load(f)

        self.intent_matcher = IntentMatcher(responses)

    def get_session(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationEngine(self.intent_matcher, session_id)
        return self.sessions[session_id]

    def process_message(self, session_id: str, message: str):
        conversation = self.get_session(session_id)

        reply = conversation.process(message)

        return reply, conversation.order_manager.status



