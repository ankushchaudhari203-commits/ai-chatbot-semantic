import json
import torch
from sentence_transformers import SentenceTransformer, util

# Load semantic model
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_responses():
    with open("responses.json", "r") as file:
        return json.load(file)

def get_best_match(user_input, responses, question_embeddings, questions):
    user_embedding = model.encode(user_input, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(user_embedding, question_embeddings)

    best_match_index = torch.argmax(similarities)
    best_score = similarities[0][best_match_index]

    if best_score > 0.5:
        return responses[questions[best_match_index]]
    else:
        return "I'm not sure I understand. Could you rephrase?"

def main():
    print("🤖 AI Semantic Chatbot (type 'exit' to quit)")
    responses = load_responses()

    questions = list(responses.keys())
    question_embeddings = model.encode(questions, convert_to_tensor=True)

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Bot: Goodbye! 👋")
            break

        response = get_best_match(user_input, responses, question_embeddings, questions)
        print("Bot:", response)

if __name__ == "__main__":
    main()

