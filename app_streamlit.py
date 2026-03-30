"""
🚀 AstroHealth AI — Streamlit Chatbot Interface

Knowledge-Grounded & Explainable AI Framework
for Astronaut Health Monitoring and Performance Optimization.

Run with:  streamlit run app_streamlit.py
"""

import streamlit as st
from openai import OpenAI

from config import (
    APP_ICON, APP_SUBTITLE, APP_TITLE, AVAILABLE_MODELS,
    DEFAULT_MODEL, OPENAI_API_KEY, SAMPLE_QUESTIONS, SYSTEM_PROMPT,
)
from explainability import (
    extract_main_response, format_explainability_text,
    get_confidence_color, get_confidence_emoji, parse_explainability,
)
from knowledge_base import (
    format_knowledge_context, get_all_topics, retrieve_relevant_knowledge,
)

# ─── Page Configuration ─────────────────────────────────────────────
st.set_page_config(
    page_title="AstroHealth AI",
    page_icon="🧑‍🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global Dark Space Theme ── */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 40%, #0d1117 100%);
    }

    /* ── Header Styling ── */
    .main-header {
        text-align: center;
        padding: 1.5rem 0 1rem;
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(139, 92, 246, 0.1));
        border-radius: 16px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        margin-bottom: 1.5rem;
    }
    .main-header h1 {
        font-size: 2.2rem;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .main-header p {
        color: #94a3b8;
        font-size: 0.95rem;
        margin: 0.3rem 0 0;
    }

    /* ── Chat Messages ── */
    .stChatMessage {
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        backdrop-filter: blur(10px);
    }

    /* ── Explainability Panel ── */
    .explain-panel {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-top: 0.5rem;
    }
    .explain-header {
        font-size: 0.85rem;
        color: #38bdf8;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .confidence-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%);
        border-right: 1px solid rgba(56, 189, 248, 0.15);
    }

    /* ── Sample Question Buttons ── */
    .sample-btn {
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        color: #cbd5e1;
        cursor: pointer;
        font-size: 0.82rem;
        transition: all 0.2s;
        width: 100%;
        text-align: left;
    }
    .sample-btn:hover {
        background: rgba(56, 189, 248, 0.2);
        border-color: #38bdf8;
        color: #f1f5f9;
    }

    /* ── Knowledge Topics Pills ── */
    .topic-pill {
        display: inline-block;
        background: rgba(139, 92, 246, 0.15);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        padding: 3px 12px;
        margin: 2px 3px;
        font-size: 0.75rem;
        color: #c4b5fd;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        color: #475569;
        font-size: 0.75rem;
        padding: 1rem 0;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# ─── Session State Initialization ────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "explain_data" not in st.session_state:
    st.session_state.explain_data = {}  # msg_index -> explainability dict


# ─── Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"## {APP_ICON} AstroHealth AI")
    st.caption("v1.0 · Knowledge-Grounded & Explainable")

    st.markdown("---")

    # API key loaded from .env or environment variable (not shown in UI)
    api_key = OPENAI_API_KEY

    # Model Selection
    st.markdown("### 🤖 Model")
    model = st.selectbox(
        "Select model",
        AVAILABLE_MODELS,
        index=AVAILABLE_MODELS.index(DEFAULT_MODEL),
    )

    # Temperature
    temperature = st.slider(
        "Temperature", 0.0, 1.5, 0.4, 0.1,
        help="Higher = more creative, Lower = more precise",
    )

    st.markdown("---")

    # Knowledge Base Topics
    st.markdown("### 📚 Knowledge Base")
    topics = get_all_topics()
    topic_html = "".join(f'<span class="topic-pill">{t}</span>' for t in topics)
    st.markdown(f'<div style="line-height:2.2">{topic_html}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Controls
    st.markdown("### ⚙️ Controls")
    show_explain = st.toggle("Show Explainability", value=True)

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.explain_data = {}
        st.rerun()

    # Footer
    st.markdown(
        '<div class="footer">Built with Streamlit + OpenAI<br>'
        "Knowledge-Grounded AI Framework</div>",
        unsafe_allow_html=True,
    )


# ─── Main Content ────────────────────────────────────────────────────
st.markdown(
    f'<div class="main-header">'
    f"<h1>{APP_TITLE}</h1>"
    f"<p>{APP_SUBTITLE}</p>"
    f"</div>",
    unsafe_allow_html=True,
)

# ─── Display Chat History ────────────────────────────────────────────
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"], avatar="🧑‍🚀" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

        # Show explainability for assistant messages
        if msg["role"] == "assistant" and show_explain and idx in st.session_state.explain_data:
            exp = st.session_state.explain_data[idx]
            with st.expander("🔍 Explainability Details", expanded=False):
                conf = exp.get("confidence", "UNKNOWN")
                emoji = get_confidence_emoji(conf)
                color = get_confidence_color(conf)

                st.markdown(
                    f'<span class="confidence-badge" style="background:{color}22;'
                    f'color:{color};border:1px solid {color}">'
                    f"{emoji} {conf} Confidence</span>",
                    unsafe_allow_html=True,
                )

                st.markdown("")

                # Sources
                sources = exp.get("sources_used", [])
                if sources:
                    st.markdown("**📚 Sources Used:**")
                    for src in sources:
                        st.markdown(f"- {src}")

                # Reasoning Chain
                chain = exp.get("reasoning_chain", [])
                if chain:
                    st.markdown("**🔗 Reasoning Chain:**")
                    for i, step in enumerate(chain, 1):
                        st.markdown(f"{i}. {step}")

                # Key Factors
                factors = exp.get("key_factors", [])
                if factors:
                    st.markdown("**🔑 Key Factors:**")
                    for f in factors:
                        st.markdown(f"- ◆ {f}")

                # Limitations
                lim = exp.get("limitations", "")
                if lim:
                    st.warning(f"⚠️ **Limitations:** {lim}")


# ─── Sample Questions (show only when no messages) ───────────────────
if not st.session_state.messages:
    st.markdown("### 💡 Try asking about:")
    cols = st.columns(2)
    for i, question in enumerate(SAMPLE_QUESTIONS):
        col = cols[i % 2]
        with col:
            if st.button(f"🔹 {question}", key=f"sample_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()


# ─── Chat Input ──────────────────────────────────────────────────────
user_input = st.chat_input("Ask about astronaut health, performance, or space medicine...")

if user_input:
    # Validate API key
    if not api_key:
        st.error("⚠️ Please enter your OpenAI API key in the sidebar to continue.")
        st.stop()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Retrieve knowledge context
    relevant_knowledge = retrieve_relevant_knowledge(user_input)
    knowledge_context = format_knowledge_context(relevant_knowledge)

    # Build messages for OpenAI
    augmented_system = (
        f"{SYSTEM_PROMPT}\n\n"
        f"═══ KNOWLEDGE CONTEXT ═══\n{knowledge_context}\n═══ END CONTEXT ═══"
    )

    openai_messages = [{"role": "system", "content": augmented_system}]

    # Include recent chat history (last 10 exchanges for context window)
    history_window = st.session_state.messages[-20:]
    for msg in history_window:
        openai_messages.append({"role": msg["role"], "content": msg["content"]})

    # Call OpenAI
    with st.chat_message("assistant", avatar="🧑‍🚀"):
        with st.spinner("🛰️ Processing with AstroHealth AI..."):
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=model,
                    messages=openai_messages,
                    temperature=temperature,
                    max_tokens=2000,
                )
                full_response = response.choices[0].message.content

                # Parse explainability
                explain = parse_explainability(full_response)
                main_answer = extract_main_response(full_response)

                # Display main answer
                st.markdown(main_answer)

                # Store message and explainability
                msg_idx = len(st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": main_answer})

                if explain:
                    st.session_state.explain_data[msg_idx] = explain

                    # Show live explainability
                    if show_explain:
                        with st.expander("🔍 Explainability Details", expanded=True):
                            conf = explain.get("confidence", "UNKNOWN")
                            emoji = get_confidence_emoji(conf)
                            color = get_confidence_color(conf)

                            st.markdown(
                                f'<span class="confidence-badge" style="background:{color}22;'
                                f'color:{color};border:1px solid {color}">'
                                f"{emoji} {conf} Confidence</span>",
                                unsafe_allow_html=True,
                            )
                            st.markdown("")

                            sources = explain.get("sources_used", [])
                            if sources:
                                st.markdown("**📚 Sources Used:**")
                                for src in sources:
                                    st.markdown(f"- {src}")

                            chain = explain.get("reasoning_chain", [])
                            if chain:
                                st.markdown("**🔗 Reasoning Chain:**")
                                for i, step in enumerate(chain, 1):
                                    st.markdown(f"{i}. {step}")

                            factors = explain.get("key_factors", [])
                            if factors:
                                st.markdown("**🔑 Key Factors:**")
                                for f in factors:
                                    st.markdown(f"- ◆ {f}")

                            lim = explain.get("limitations", "")
                            if lim:
                                st.warning(f"⚠️ **Limitations:** {lim}")

            except Exception as e:
                st.error(f"❌ Error communicating with OpenAI: {str(e)}")
