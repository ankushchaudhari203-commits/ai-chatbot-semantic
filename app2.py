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
    order_manager = memory["order_manager"]

    # 🧠 Handle checkout state
    if order_manager.status == "completed":
        return "Your order has already been completed. Start a new order if you'd like!"

    if order_manager.status == "checkout":
        if "confirm" in lower_input:
            order_manager.status = "completed"
            return "Order confirmed! Thank you for your purchase."
        return "You are at checkout. Type 'confirm' to complete the order."
        
    if "confirm payment" in lower_input:
        return order_manager.confirm_payment()
        
    if "confirm payment" in lower_input or "paid" in lower_input:
        return order_manager.finalize_order()



    # Remove last item
    if "remove" in lower_input:
        return order_manager.remove_last_item()

    # Clear order
    if "clear" in lower_input or "cancel" in lower_input:
        return order_manager.clear_order()

    # Checkout
    if "checkout" in lower_input or "pay" in lower_input:
        return order_manager.checkout()

    # Summary
    if "summary" in lower_input or "my order" in lower_input:
        return order_manager.get_summary()

    # Slot filling for size
    if "large" in lower_input:
        memory["size"] = "Large"
    elif "medium" in lower_input:
        memory["size"] = "Medium"
    elif "small" in lower_input:
        memory["size"] = "Small"

    # Slot filling for type
    if "pepperoni" in lower_input:
        memory["type"] = "Pepperoni"
    elif "veggie" in lower_input:
        memory["type"] = "Veggie"
    elif "cheese" in lower_input:
        memory["type"] = "Cheese"
    elif "buffalo" in lower_input:
        memory["type"] = "Buffalo Chicken"

    # If both collected → add item
    if memory["size"] and memory["type"]:
        response = order_manager.add_item(memory["type"], memory["size"])
        memory["size"] = None
        memory["type"] = None
        return response

    # Fallback to AI intent detection
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
    
#def remove_last_item(memory):
    #items = memory["order"]["items"]

    #if not items:
        #return "Your order is already empty."

    #removed_item = items.pop()

    #return f"Removed {removed_item['size']} {removed_item['type']} from your order."

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

class OrderManager:
    def __init__(self):
        self.items = []
        self.status = "building"

    def add_item(self, pizza_type, size):
        price = PIZZA_PRICES.get(pizza_type, {}).get(size)

        if not price:
            return "Pricing not available."

        item = {
            "type": pizza_type,
            "size": size,
            "price": price
        }

        self.items.append(item)
        return f"{size} {pizza_type} added. Price: ${price:.2f}"

    def remove_last_item(self):
        if not self.items:
            return "Your order is empty."

        removed = self.items.pop()
        return f"Removed {removed['size']} {removed['type']}."

    def clear_order(self):
        self.items = []
        return "Your order has been cleared."

    def get_summary(self):
        if not self.items:
            return "Your order is empty."

        total = 0
        lines = []

        for item in self.items:
            total += item["price"]
            lines.append(f"{item['size']} {item['type']} - ${item['price']:.2f}")

        summary = "\n".join(lines)
        return f"Your order:\n{summary}\n\nTotal: ${total:.2f}"

    def checkout(self):
        if not self.items:
            return "Cannot checkout. Your order is empty."

        self.status = "checkout"
        return self.get_summary() + "\n\nProceeding to payment..."

    
    def confirm_payment(self):
        if self.status != "checkout":
            return "You must checkout first."

        self.status = "completed"
        return "Payment confirmed! Your order is being prepared."
        
    def finalize_order(self):
        if self.status != "checkout":
            return "You must checkout before finalizing payment."

        self.status = "completed"
        return "Payment confirmed! Your order is now being prepared."




def main():
    print("🤖 AI Context-Aware Chatbot (type 'exit' to quit)")
    responses = load_responses()
    intent_embeddings = prepare_intent_embeddings(responses)

    # Context memory
    session_memory = {
        "intent": None,
            "intent": None,
            "size": None,
            "type" : None,
            "order_manager": OrderManager()
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
