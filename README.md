# 🚀 AstroHealth AI — Astronaut Health Monitoring Chatbot

**Knowledge-Grounded & Explainable AI Framework for Astronaut Health Monitoring and Performance Optimization**

A dual-interface chatbot (Streamlit + Gradio) powered by OpenAI that provides expert-level, explainable answers about astronaut health, space medicine, and crew performance optimization.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **Knowledge-Grounded AI** | Curated domain knowledge covering 10 astronaut health topics |
| 🔍 **Explainability Engine** | Shows confidence level, sources used, reasoning chain, and key factors |
| 🖥️ **Streamlit Interface** | Rich dark-themed UI with sidebar controls and chat history |
| 🎛️ **Gradio Interface** | Alternative lightweight chat UI with settings panel |
| 🔑 **Flexible API Key** | Via `.env` file or real-time sidebar input |
| 💡 **Sample Questions** | Quick-start prompts for exploring astronaut health topics |

### Knowledge Base Topics

1. Cardiovascular Deconditioning
2. Bone Density Loss & Musculoskeletal Health
3. Space Radiation Exposure
4. Sleep & Circadian Rhythm Disruption
5. Spaceflight Associated Neuro-ocular Syndrome (SANS)
6. Psychological Health & Behavioral Performance
7. Exercise Protocols & Physical Fitness
8. Nutrition & Hydration in Space
9. Immune System Changes in Space
10. Performance Metrics & Crew Readiness

---

## 📋 Prerequisites

- **Python 3.9+** (recommended: 3.11+)
- **OpenAI API Key** — Get one at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **pip** (Python package installer)

---

## 🛠️ Step-by-Step Setup Guide

### Step 1: Open Terminal

Open a terminal (Command Prompt / PowerShell / Terminal) and navigate to the project directory:

```bash
cd path/to/AstronautHealthChatbot
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` — Primary chat UI framework
- `gradio` — Alternative chat UI framework
- `openai` — OpenAI API client for GPT models
- `python-dotenv` — Environment variable loading from `.env`

### Step 4: Configure Your API Key

**Option A** — Create a `.env` file (recommended for repeated use):

```bash
# Copy the template
cp .env.example .env

# Edit the .env file and replace the placeholder with your real key:
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Option B** — Enter it directly in the app sidebar when running (no `.env` needed).

### Step 5: Run the Streamlit App (Primary Interface)

```bash
streamlit run app_streamlit.py
```

This will:
- Start a local web server (usually at `http://localhost:8501`)
- Automatically open the app in your default browser
- Show the space-themed chat interface

### Step 6: Run the Gradio App (Alternative Interface)

```bash
python app_gradio.py
```

This will:
- Start a local web server at `http://localhost:7860`
- Open the Gradio chat interface in your browser

> **Note:** Run only one app at a time, or use different terminal windows.

---

## 🎯 How to Use

1. **Enter your API key** (if not configured via `.env`) in the sidebar/settings panel
2. **Select a model** — `gpt-4o-mini` is the default (fast & affordable); `gpt-4o` for best quality
3. **Ask a question** — Type about astronaut health, or click a sample question
4. **Review the answer** — The AI provides a structured, knowledge-grounded response
5. **Check explainability** — Expand the "Explainability Details" panel to see:
   - 🟢🟡🔴 **Confidence Level** (High / Medium / Low)
   - 📚 **Sources Used** — Which knowledge base topics were referenced
   - 🔗 **Reasoning Chain** — Step-by-step logic the AI followed
   - 🔑 **Key Factors** — Important elements that shaped the answer
   - ⚠️ **Limitations** — Caveats about the response

---

## 🏗️ Project Architecture

```
AstronautHealthChatbot/
│
├── app_streamlit.py      ← Streamlit chatbot (primary UI)
├── app_gradio.py         ← Gradio chatbot (alternative UI)
│
├── knowledge_base.py     ← Domain knowledge + retrieval engine
├── explainability.py     ← Parses AI reasoning & confidence
├── config.py             ← Settings, system prompt, sample questions
│
├── requirements.txt      ← Python dependencies
├── .env.example          ← API key template
└── README.md             ← This file
```

### How It Works

```
User Question
     │
     ▼
┌─────────────────────┐
│  Knowledge Retrieval │ ◄── knowledge_base.py
│  (keyword matching)  │     Finds relevant health topics
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Augmented Prompt    │ ◄── config.py
│  System + Context    │     Injects knowledge into prompt
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  OpenAI GPT Model   │ ◄── openai API
│  (gpt-4o-mini, etc) │     Generates grounded response
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Explainability      │ ◄── explainability.py
│  Parser              │     Extracts confidence, sources, reasoning
└────────┬────────────┘
         │
         ▼
   Chat UI (Streamlit / Gradio)
   Shows answer + explainability panel
```

---

## 💡 Tips

- **Cost optimization**: Use `gpt-4o-mini` for most queries — it's fast and very affordable
- **Better answers**: Lower the temperature (0.2-0.3) for factual, precise responses
- **Creative exploration**: Raise temperature (0.7-1.0) for broader discussions
- **Follow-ups**: The chatbot maintains conversation history, so ask follow-up questions naturally
- **Out of scope**: If you ask non-health questions, the bot will politely redirect you

---

## 🔧 Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| API key error | Check your `.env` file or enter the key in the sidebar |
| Port already in use | Kill the existing process or change the port |
| Slow responses | Switch to `gpt-4o-mini` (faster) or check your internet |

---

## 📜 License

This project is for educational and research purposes.

Built with ❤️ using Streamlit, Gradio, and OpenAI.
