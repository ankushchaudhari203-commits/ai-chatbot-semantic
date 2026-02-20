from app.engine.order_manager import OrderManager

class ChatbotEngine:

    def __init__(self, intent_matcher):
        self.intent_matcher = intent_matcher
        self.order_manager = OrderManager()

    def get_total(self):
        return self.order_manager.get_total()

    def get_items(self):
        return self.order_manager.get_items()


class ConversationEngine:
    
    def __init__(self, intent_matcher, session_id):
        self.intent_matcher = intent_matcher
        self.order_manager = OrderManager()
        self.order_manager.session_id = session_id
        self.size = None
        self.type = None


    def process(self, user_input):
        lower_input = user_input.lower()

        # ===== Order Commands =====
        if "remove" in lower_input:
            return self.order_manager.remove_last_item()

        if "clear" in lower_input or "cancel" in lower_input:
            return self.order_manager.clear_order()

        if "checkout" in lower_input:
            return self.order_manager.checkout()

        if "confirm payment" in lower_input or "paid" in lower_input:
            return self.order_manager.confirm_payment()

        if "summary" in lower_input or "my order" in lower_input:
            return self.order_manager.get_summary()

        # ===== Prevent modifications after checkout =====
        if self.order_manager.status != "building":
            return self.intent_matcher.match(user_input)

        # ===== Slot Filling =====
        if "large" in lower_input:
            self.size = "Large"
        elif "medium" in lower_input:
            self.size = "Medium"
        elif "small" in lower_input:
            self.size = "Small"

        if "pepperoni" in lower_input:
            self.type = "Pepperoni"
        elif "veggie" in lower_input:
            self.type = "Veggie"
        elif "cheese" in lower_input:
            self.type = "Cheese"
        elif "buffalo" in lower_input:
            self.type = "Buffalo Chicken"

        if self.size and self.type:
            response = self.order_manager.add_item(self.type, self.size)
            self.size = None
            self.type = None
            return response

        # ===== Fallback =====
        return self.intent_matcher.match(user_input)
