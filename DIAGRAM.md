1. User Input Layer
Handles interaction via CLI (with future support for macOS/iOS UI).
This layer only collects input and displays responses — no business logic.


2. Conversation Engine
The central orchestration layer that manages:
Context handling
Conversation memory
Slot filling (size, type, toppings extraction)
It determines whether the input should update order state or be routed to
the intent engine.


3. Intent-Based Semantic Engine
Responsible for understanding user meaning using:
Precomputed sentence embeddings
Cosine similarity for intent recognition
This enables semantic understanding instead of simple keyword matching.


4. Knowledge Layer
Stores conversational intents and pattern variations in a structured JSON
configuration file.
This keeps natural language data separate from application logic.


5. Order Management Layer
Maintains structured order state:
Multi-item tracking
Order status management
Allows complex multi-turn order building.


6. Dynamic Pricing Engine
Calculates real-time pricing based on:
Pizza size
Pizza type
Multiple items
Ensures business logic is separate from conversational logic.
