"""
🚀 AstroHealth AI — Gradio Chatbot Interface

Knowledge-Grounded & Explainable AI Framework
for Astronaut Health Monitoring and Performance Optimization.

Run with:  python app_gradio.py
"""

import gradio as gr
from openai import OpenAI

from config import (
    APP_SUBTITLE, AVAILABLE_MODELS, DEFAULT_MODEL,
    OPENAI_API_KEY, SAMPLE_QUESTIONS, SYSTEM_PROMPT,
)
from explainability import (
    extract_main_response, format_explainability_text, parse_explainability,
)
from knowledge_base import (
    format_knowledge_context, get_all_topics, retrieve_relevant_knowledge,
)


# ─── Core Chat Function ─────────────────────────────────────────────

def chat(
    message: str,
    history: list,
    api_key: str,
    model: str,
    temperature: float,
):
    """
    Process user message through the knowledge-grounded AI pipeline.
    Returns (assistant_reply, explainability_text).
    """
    # Validate API key
    key = api_key.strip() or OPENAI_API_KEY
    if not key:
        return (
            "⚠️ **Please enter your OpenAI API key** in the settings panel above to start chatting.",
            "No API key provided.",
        )

    # Retrieve relevant knowledge
    relevant = retrieve_relevant_knowledge(message)
    context = format_knowledge_context(relevant)

    # Build system prompt with knowledge context
    augmented_system = (
        f"{SYSTEM_PROMPT}\n\n"
        f"═══ KNOWLEDGE CONTEXT ═══\n{context}\n═══ END CONTEXT ═══"
    )

    # Build messages list
    messages = [{"role": "system", "content": augmented_system}]

    # Add recent history (last 10 exchanges)
    for user_msg, bot_msg in (history or [])[-10:]:
        messages.append({"role": "user", "content": user_msg})
        if bot_msg:
            messages.append({"role": "assistant", "content": bot_msg})

    messages.append({"role": "user", "content": message})

    # Call OpenAI
    try:
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=2000,
        )
        full_response = response.choices[0].message.content

        # Parse explainability and clean response
        explain = parse_explainability(full_response)
        main_answer = extract_main_response(full_response)
        explain_text = format_explainability_text(explain) if explain else "No explainability data in this response."

        return main_answer, explain_text

    except Exception as e:
        return f"❌ **Error:** {str(e)}", f"Error occurred: {str(e)}"


# ─── Gradio Interface Builder ────────────────────────────────────────

def create_gradio_app():
    """Build and return the Gradio Blocks interface."""

    # Custom CSS for dark space theme
    custom_css = """
    .gradio-container {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 40%, #0d1117 100%) !important;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    .main-title {
        text-align: center;
        padding: 1.2rem;
        background: linear-gradient(135deg, rgba(56,189,248,0.1), rgba(139,92,246,0.1));
        border-radius: 16px;
        border: 1px solid rgba(56,189,248,0.2);
        margin-bottom: 1rem;
    }
    .main-title h1 {
        font-size: 2rem;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .main-title p {
        color: #94a3b8;
        margin: 0.3rem 0 0;
    }
    .explain-box {
        background: rgba(15, 23, 42, 0.9) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 12px !important;
        font-family: 'Fira Code', 'Consolas', monospace !important;
        font-size: 0.85rem !important;
    }
    .topic-list {
        color: #c4b5fd;
        font-size: 0.85rem;
        line-height: 2;
    }
    footer { display: none !important; }
    """

    with gr.Blocks(
        title="AstroHealth AI",
        css=custom_css,
        theme=gr.themes.Base(
            primary_hue="sky",
            secondary_hue="violet",
            neutral_hue="slate",
            font=gr.themes.GoogleFont("Inter"),
        ).set(
            body_background_fill="*neutral_950",
            body_text_color="*neutral_200",
            block_background_fill="*neutral_900",
            block_border_color="*neutral_700",
            input_background_fill="*neutral_800",
            button_primary_background_fill="*primary_600",
            button_primary_text_color="white",
        ),
    ) as app:

        # ── Header ──
        gr.HTML(
            '<div class="main-title">'
            "<h1>🚀 AstroHealth AI</h1>"
            f"<p>{APP_SUBTITLE}</p>"
            "</div>"
        )

        with gr.Row():
            # ── Left Column: Settings ──
            with gr.Column(scale=1, min_width=280):
                gr.Markdown("### ⚙️ Settings")

                api_key_input = gr.Textbox(
                    label="🔑 OpenAI API Key",
                    placeholder="sk-...",
                    type="password",
                    value=OPENAI_API_KEY or "",
                )

                model_dropdown = gr.Dropdown(
                    choices=AVAILABLE_MODELS,
                    value=DEFAULT_MODEL,
                    label="🤖 Model",
                )

                temp_slider = gr.Slider(
                    minimum=0.0, maximum=1.5, value=0.4, step=0.1,
                    label="🌡️ Temperature",
                )

                gr.Markdown("---")
                gr.Markdown("### 📚 Knowledge Topics")
                topics_text = "\n".join(f"• {t}" for t in get_all_topics())
                gr.Markdown(f'<div class="topic-list">{topics_text}</div>')

            # ── Right Column: Chat ──
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    label="💬 Chat",
                    height=450,
                    show_copy_button=True,
                    avatar_images=("👤", "🧑‍🚀"),
                    type="messages",
                )

                with gr.Row():
                    msg_input = gr.Textbox(
                        placeholder="Ask about astronaut health, performance, or space medicine...",
                        label="Your Message",
                        scale=5,
                        show_label=False,
                    )
                    send_btn = gr.Button("🚀 Send", variant="primary", scale=1)

                # ── Explainability Accordion ──
                with gr.Accordion("🔍 Explainability Details", open=False):
                    explain_output = gr.Textbox(
                        label="",
                        lines=12,
                        interactive=False,
                        elem_classes=["explain-box"],
                    )

                # ── Sample Questions ──
                gr.Markdown("### 💡 Sample Questions")
                with gr.Row():
                    sample_btns = []
                    for i, q in enumerate(SAMPLE_QUESTIONS[:4]):
                        btn = gr.Button(
                            f"🔹 {q}",
                            size="sm",
                            variant="secondary",
                        )
                        sample_btns.append((btn, q))

        # ── State for chat history (internal format for OpenAI) ──
        chat_history_state = gr.State([])

        # ── Event Handlers ──
        def respond(message, chat_history_internal, api_key, model, temperature):
            if not message.strip():
                return "", chat_history_internal, [], "Please enter a message."

            # Get AI response
            answer, explain_text = chat(
                message, chat_history_internal, api_key, model, temperature,
            )

            # Update internal history (tuple format for OpenAI)
            chat_history_internal = chat_history_internal or []
            chat_history_internal.append((message, answer))

            # Build display messages (messages format for Chatbot)
            display_messages = []
            for user_msg, bot_msg in chat_history_internal:
                display_messages.append({"role": "user", "content": user_msg})
                if bot_msg:
                    display_messages.append({"role": "assistant", "content": bot_msg})

            return "", chat_history_internal, display_messages, explain_text

        # Send button click
        send_btn.click(
            respond,
            inputs=[msg_input, chat_history_state, api_key_input, model_dropdown, temp_slider],
            outputs=[msg_input, chat_history_state, chatbot, explain_output],
        )

        # Enter key submit
        msg_input.submit(
            respond,
            inputs=[msg_input, chat_history_state, api_key_input, model_dropdown, temp_slider],
            outputs=[msg_input, chat_history_state, chatbot, explain_output],
        )

        # Sample question buttons
        def use_sample(question, chat_history_internal, api_key, model, temperature):
            return respond(question, chat_history_internal, api_key, model, temperature)

        for btn, question in sample_btns:
            btn.click(
                lambda q=question: q,
                outputs=[msg_input],
            ).then(
                respond,
                inputs=[msg_input, chat_history_state, api_key_input, model_dropdown, temp_slider],
                outputs=[msg_input, chat_history_state, chatbot, explain_output],
            )

    return app


# ─── Main Entry Point ───────────────────────────────────────────────
if __name__ == "__main__":
    app = create_gradio_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
    )
