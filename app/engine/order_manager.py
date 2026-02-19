from pricing import PIZZA_PRICES
from app.db.database import get_connection





class OrderManager:
    def __init__(self):
        self.items = []
        self.status = "building"

    def add_item(self, pizza_type, size):
        if self.status != "building":
            return "You cannot modify the order after checkout."
        
        price = PIZZA_PRICES.get(pizza_type, {}).get(size)

        if not price:
            return "Pricing not available."

        item = {
            "type": pizza_type,
            "size": size,
            "price": price
        }

        self.items.append(item)

        # Save to DB
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO orders (session_id, item_type, size, price, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            getattr(self, "session_id", "unknown"),
            pizza_type,
            size,
            price,
            self.status
        ))

        conn.commit()
        conn.close()

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
            
        if self.status == "completed":
            return "Your order has already been completed."

        self.status = "checkout"
        return self.get_summary() + "\n\nProceeding to payment..."

    def finalize_order(self):
        if self.status != "checkout":
            return "You must checkout before finalizing payment."

        self.status = "completed"
        return "Payment confirmed! Your order is now being prepared."
        
    def confirm_payment(self):
        if self.status != "checkout":
            return "You need to checkout first."

        self.status = "completed"
        return "Payment confirmed! Your order is now being prepared."

