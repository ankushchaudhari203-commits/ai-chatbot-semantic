import json
import torch
from sentence_transformers import SentenceTransformer, util

# Load semantic model
model = SentenceTransformer("all-MiniLM-L6-v2")

PIZZA_PRICES = {
    "Pepperoni": {
        "Small": 14.99,
        "Medium": 18.99,
        "Large": 22.08
    },
    "Veggie": {
        "Small": 13.99,
        "Medium": 17.99,
        "Large": 18.09
    },
    "Cheese": {
        "Small": 12.99,
        "Medium": 15.99,
        "Large": 15.07
    },
    "Buffalo Chicken": {
        "Small": 15.99,
        "Medium": 19.99,
        "Large": 20.51
    }
}


def load_responses():
    with open("responses.json", "r") as file:
        return json.load(file)

def get_best_match(user_input, intent_embeddings):
    user_embedding = model.encode(user_input, convert_to_tensor=True)

    best_score = 0
    best_response = None

    for intent in intent_embeddings:
        similarities = util.pytorch_cos_sim(user_embedding, intent["embeddings"])
        max_score = torch.max(similarities)

        if max_score > best_score:
            best_score = max_score
            best_response = intent["response"]

    if best_score > 0.5:
        return best_response
    else:
        return "I'm not sure I understand. Could you rephrase?"


def handle_conversation(user_input, intent_embeddings, memory):

    lower_input = user_input.lower()

    # Remove last item
    if "remove" in lower_input:
        return remove_last_item(memory)

    # Order summary
    if "summary" in lower_input or "my order" in lower_input:
        return generate_order_summary(memory)

    # Clear order
    if "clear order" in lower_input or "cancel order" in lower_input:
        memory["order"]["items"] = []
        return "Your order has been cleared."

    # Checkout
    if "checkout" in lower_input or "pay" in lower_input:
        memory["order"]["status"] = "checkout"
        return generate_order_summary(memory) + "\n\nProceeding to checkout..."

    # Detect pizza size
    if "large" in lower_input:
        memory["order"]["size"] = "Large"
    elif "medium" in lower_input:
        memory["order"]["size"] = "Medium"
    elif "small" in lower_input:
        memory["order"]["size"] = "Small"

    # Detect pizza type
    if "pepperoni" in lower_input:
        memory["order"]["type"] = "Pepperoni"
    elif "veggie" in lower_input:
        memory["order"]["type"] = "Veggie"
    elif "cheese" in lower_input:
        memory["order"]["type"] = "Cheese"
    elif "buffalo" in lower_input:
        memory["order"]["type"] = "Buffalo Chicken"

    # Confirm order if both size and type exist
    if memory["order"]["size"] and memory["order"]["type"]:

        size = memory["order"]["size"]
        ptype = memory["order"]["type"]

        price = PIZZA_PRICES.get(ptype, {}).get(size)

        if price:
            item = {
                "type": ptype,
                "size": size,
                "price": price
            }

            memory["order"]["items"].append(item)

            memory["order"]["size"] = None
            memory["order"]["type"] = None

            return f"{size} {ptype} pizza added. Price: ${price:.2f}"

        else:
            return "Sorry, pricing not available."

    # Fallback to semantic intent matching
    return get_best_match(user_input, intent_embeddings)


def generate_order_summary(memory):
    items = memory["order"]["items"]

    if not items:
        return "Your order is currently empty."

    total = 0
    summary_lines = []

    for item in items:
        total += item["price"]
        summary_lines.append(
            f"{item['size']} {item['type']} - ${item['price']:.2f}"
        )

    summary_text = "\n".join(summary_lines)

    return f"Your order:\n{summary_text}\n\nTotal: ${total:.2f}"
    
def remove_last_item(memory):
    items = memory["order"]["items"]

    if not items:
        return "Your order is already empty."

    removed_item = items.pop()

    return f"Removed {removed_item['size']} {removed_item['type']} from your order."

def prepare_intent_embeddings(responses):
    intent_embeddings = []

    for intent_name, intent_data in responses.items():
        patterns = intent_data["patterns"]
        embeddings = model.encode(patterns, convert_to_tensor=True)

        intent_embeddings.append({
            "intent": intent_name,
            "response": intent_data["response"],
            "patterns": patterns,
            "embeddings": embeddings
        })

    return intent_embeddings

def main():
    print("🤖 AI Context-Aware Chatbot (type 'exit' to quit)")
    responses = load_responses()
    intent_embeddings = prepare_intent_embeddings(responses)

    # Context memory
    session_memory = {
        "intent": None,
        "order": {
            "size": None,
            "type": None,
            "addons": [],
            "items": [],
            "status": "building"
        },
        "last_question": None
    }

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Bot: Goodbye! 👋")
            break

        response = handle_conversation(
            user_input,
            intent_embeddings,
            session_memory
        )

        print("Bot:", response)

if __name__ == "__main__":
    main()
