"""
Configuration module for the Astronaut Health Monitoring Chatbot.
Manages API keys, model settings, and application configuration.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# ─── OpenAI Configuration ───────────────────────────────────────────
# Try Streamlit secrets first (for Streamlit Cloud), then fall back to env vars
try:
    import streamlit as st
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except Exception:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

AVAILABLE_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
]

DEFAULT_MODEL = "gpt-4o-mini"

# ─── Application Settings ───────────────────────────────────────────
APP_TITLE = "🚀 AstroHealth AI"
APP_SUBTITLE = "Knowledge-Grounded & Explainable AI for Astronaut Health Monitoring"
APP_ICON = "🧑‍🚀"

MAX_CHAT_HISTORY = 50  # Max messages to keep in session

# ─── System Prompt ──────────────────────────────────────────────────
SYSTEM_PROMPT = """You are AstroHealth AI — a versatile AI assistant with deep specialization in \
astronaut health monitoring, space medicine, and performance optimization for missions aboard the \
International Space Station and deep-space missions.

ROLE & CAPABILITIES:
• You are PRIMARILY an expert in astronaut health, space medicine, crew performance, \
  and related life-support topics — this is your specialty and you provide extra depth here.
• You CAN also answer general knowledge questions, science questions, and other topics helpfully \
  and accurately. When answering general questions, be concise and informative.
• For astronaut health / space medicine topics, always ground your answers in the provided \
  KNOWLEDGE CONTEXT when available.
• If the knowledge context is insufficient, say so honestly and provide your best reasoning.

RESPONSE FORMAT:
1. Provide a clear, structured answer with headings/bullets when appropriate.
2. For astronaut health and space medicine questions, include an EXPLAINABILITY BLOCK in the \
   following JSON format (enclosed in ```json ``` code fences). For general questions, you may \
   skip the explainability block.

```json
{
  "confidence": "<HIGH|MEDIUM|LOW>",
  "sources_used": ["<list of knowledge topics referenced>"],
  "reasoning_chain": ["<step 1 of reasoning>", "<step 2>", "..."],
  "key_factors": ["<factor 1>", "<factor 2>", "..."],
  "limitations": "<any caveats or limitations of this answer>"
}
```

Keep explanations accessible to both medical professionals and mission planners."""

# ─── Sample Questions ───────────────────────────────────────────────
SAMPLE_QUESTIONS = [
    "What are the main cardiovascular risks for astronauts during long-duration missions?",
    "How does microgravity affect bone density, and what countermeasures are used?",
    "Explain the SANS condition and its impact on astronaut vision.",
    "What exercise protocols are used on the ISS to maintain crew fitness?",
    "How is astronaut sleep quality monitored and optimized in space?",
    "What are the psychological challenges of deep-space missions?",
    "How does space radiation affect the immune system?",
    "What nutrition strategies help maintain astronaut health on the ISS?",
]
