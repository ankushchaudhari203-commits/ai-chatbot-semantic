Chat-Bot: Semantic Edition
An intent-based conversational engine that enables natural-language pizza
ordering with context awareness and dynamic pricing.


Overview
Chat-Bot has evolved from rule-based keyword matching to embedding-driven
semantic understanding. The system interprets user intent using vector
similarity, maintains session-level conversation state, and manages
multi-item orders with dynamic pricing — all through natural text
interaction.


What It Does
• Order pizza — Place orders using natural conversational language
• Browse menu — View available pizzas and pricing
• Manage cart — Add, remove, or clear items before checkout
• Generate summaries — View detailed order breakdown and total cost
• Context awareness — Maintains session memory for multi-turn conversations
• Order lifecycle management — Tracks order states from building to checkout


What’s New in This Version
• Semantic intent matching — Embedding-based similarity replaces keyword
matching
• Precomputed embeddings — Optimized performance for faster intent
recognition
• Context memory — Slot filling for size, type, and order state tracking
• Dynamic pricing engine — Calculates totals based on selections
• Stateful order lifecycle — Controlled transition from building → checkout → completed
• Multi-item cart system — Supports multiple pizzas per session


How It Works
The chatbot uses an intent-based architecture where user input is converted
into 
embeddings and compared against precomputed intent pattern vectors. A
context engine maintains session memory, enabling slot filling and
multi-turn conversation handling. A pricing module calculates totals
dynamically, while a state manager enforces order lifecycle rules.


Requirements
• Python 3.x
• sentence-transformers
• torch


Getting Started
1. Clone the repository
2. Install dependencies:
3. pip install -r requirements.txt
Run the chatbot:
python app.py
4. Start ordering via conversational prompts


Architecture
Intent Recognition — Embedding-based semantic similarity
Context Engine — Session-level memory & slot filling
Pricing Module — Structured business logic for cost calculation
Order State Manager — Lifecycle enforcement and cart management


Future Enhancements
• API service layer (FastAPI)
• SwiftUI macOS/iOS interface
• Extended order management features
• Optional LLM integration for generative responses
