"""
Explainability Engine for the Astronaut Health Monitoring Chatbot.

Parses the structured explainability block from the AI response,
providing transparency about sources, confidence, reasoning chain,
and limitations.
"""

import json
import re


def parse_explainability(response_text: str) -> dict | None:
    """
    Extracts the JSON explainability block from the AI response.
    
    Expected format in the response:
    ```json
    {
        "confidence": "HIGH|MEDIUM|LOW",
        "sources_used": [...],
        "reasoning_chain": [...],
        "key_factors": [...],
        "limitations": "..."
    }
    ```
    
    Returns:
        Parsed dict or None if no valid block found.
    """
    # Try to find JSON code block
    pattern = r"```json\s*(\{.*?\})\s*```"
    match = re.search(pattern, response_text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Fallback: try to find raw JSON object
    pattern2 = r'\{\s*"confidence"\s*:.*?\}'
    match2 = re.search(pattern2, response_text, re.DOTALL)
    if match2:
        try:
            return json.loads(match2.group(0))
        except json.JSONDecodeError:
            pass

    return None


def extract_main_response(response_text: str) -> str:
    """
    Removes the explainability JSON block from the response,
    returning only the main answer text.
    """
    # Remove ```json ... ``` block
    cleaned = re.sub(r"```json\s*\{.*?\}\s*```", "", response_text, flags=re.DOTALL)
    # Clean up extra whitespace
    cleaned = cleaned.strip()
    # Remove trailing separators
    cleaned = re.sub(r"[-─━=]{3,}\s*$", "", cleaned).strip()
    return cleaned


def get_confidence_color(confidence: str) -> str:
    """Returns a color hex code based on confidence level."""
    mapping = {
        "HIGH": "#00E676",    # Green
        "MEDIUM": "#FFD600",  # Yellow
        "LOW": "#FF5252",     # Red
    }
    return mapping.get(confidence.upper(), "#BDBDBD")


def get_confidence_emoji(confidence: str) -> str:
    """Returns an emoji indicator based on confidence level."""
    mapping = {
        "HIGH": "🟢",
        "MEDIUM": "🟡",
        "LOW": "🔴",
    }
    return mapping.get(confidence.upper(), "⚪")


def format_explainability_text(explain_data: dict) -> str:
    """
    Formats the explainability data into a readable text block
    (used for Gradio and plain-text contexts).
    """
    if not explain_data:
        return "⚠️ No explainability data available for this response."

    confidence = explain_data.get("confidence", "UNKNOWN")
    emoji = get_confidence_emoji(confidence)

    lines = [
        f"{'━' * 50}",
        f"  {emoji}  CONFIDENCE: {confidence}",
        f"{'━' * 50}",
        "",
        "📚 SOURCES USED:",
    ]

    for src in explain_data.get("sources_used", []):
        lines.append(f"   • {src}")

    lines.append("")
    lines.append("🔗 REASONING CHAIN:")
    for i, step in enumerate(explain_data.get("reasoning_chain", []), 1):
        lines.append(f"   {i}. {step}")

    lines.append("")
    lines.append("🔑 KEY FACTORS:")
    for factor in explain_data.get("key_factors", []):
        lines.append(f"   ◆ {factor}")

    limitations = explain_data.get("limitations", "")
    if limitations:
        lines.append("")
        lines.append(f"⚠️ LIMITATIONS: {limitations}")

    return "\n".join(lines)
