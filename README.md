**🍕 Chat-Bot:** Hybrid Conversational Ordering System A full-stack conversational pizza ordering system built through progressive architectural evolution — from rule-based logic to modular API design to complete frontend integration. This project demonstrates structured backend engineering, conversational UX modeling, and full-stack product thinking.

**🚀 Project Evolution (3 Phases)** This project was intentionally developed in three phases to showcase architectural growth and scalability.

**🟢 Phase 1** — Rule-Based Engine Objective: Establish conversational fundamentals. Keyword-based intent matching Basic cart handling Simple string responses Monolithic conversational logic This phase focused on understanding how conversational flows operate at a fundamental level.

**🔵 Phase 2** 
Modular API Architecture (FastAPI + Engines) Objective: Transform the chatbot into a scalable backend service. Backend Stack Python FastAPI Uvicorn JSON-based intent configuration

Engine Architecture ChatbotEngine ConversationEngine OrderManager

Component Responsibilities ChatbotEngine Handles API requests Enforces structured response contract Maintains system consistency ConversationEngine Performs intent matching Maps user input to conversational flows Uses configurable responses.json OrderManager Manages cart state Calculates dynamic pricing Controls add/remove/reset operations Handles checkout lifecycle

**🟣 Phase 3** 
Full-Stack Integration (SwiftUI + API) Objective: Deliver complete end-to-end conversational product. macOS SwiftUI frontend Real-time API integration Structured JSON rendering State synchronization between UI and backend Multi-turn conversational interaction This phase demonstrates frontend-backend contract discipline and product-level integration.

**🧠 Hybrid Conversational Design The chatbot uses a hybrid architecture combining:** Rule-based intent matching JSON-configurable questionnaire engine Modular backend separation of concerns Stateful cart lifecycle management Structured API contract enforcement The system is designed for future extensibility toward semantic or embedding-based intent matching.

**📦 Structured API Response Contract All responses follow a consistent schema:** 
{ "reply": "string", "state": "string", "total_price": 0.0, "items": [] }

Why This Matters Predictable frontend rendering Clean state transitions Clear separation of business logic and UI Scalable API design

✨ Core Features Intent-driven conversational engine 13 configurable intent categories 12–13 natural language patterns per intent JSON-based dialogue expansion without backend changes Multi-item cart management Add / remove / clear cart functionality Checkout workflow with dynamic total calculation Structured order state transitions Full-stack FastAPI + SwiftUI integration

🛠 Tech Stack Backend Python FastAPI Uvicorn JSON configuration engine Frontend SwiftUI (macOS)

🔮 Future Enhancements Semantic similarity matching (Sentence Transformers) SQLite persistence layer Order ID generation Session management Cloud deployment Optional LLM integration

🎯 What This Project Demonstrates Clean layered backend architecture Structured API contract design Conversational UX modeling State-based order lifecycle control Progressive system evolution Product-oriented engineering mindset

**Future Enhancements**
• API service layer (FastAPI)
• SwiftUI macOS/iOS interface
• Extended order management features
• Optional LLM integration for generative responses
