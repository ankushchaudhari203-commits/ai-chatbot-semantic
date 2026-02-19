import torch
from sentence_transformers import SentenceTransformer, util


class IntentMatcher:
    def __init__(self, responses):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.intent_embeddings = self._prepare_embeddings(responses)

    def _prepare_embeddings(self, responses):
        intent_embeddings = []

        for intent_name, intent_data in responses.items():
            patterns = intent_data["patterns"]
            embeddings = self.model.encode(patterns, convert_to_tensor=True)

            intent_embeddings.append({
                "intent": intent_name,
                "response": intent_data["response"],
                "embeddings": embeddings
            })

        return intent_embeddings

    def match(self, user_input):
        user_embedding = self.model.encode(user_input, convert_to_tensor=True)

        best_score = 0
        best_response = None

        for intent in self.intent_embeddings:
            similarities = util.pytorch_cos_sim(user_embedding, intent["embeddings"])
            max_score = torch.max(similarities)

            if max_score > best_score:
                best_score = max_score
                best_response = intent["response"]

        if best_score > 0.5:
            return best_response
        else:
            return "I'm not sure I understand. Could you rephrase?"

