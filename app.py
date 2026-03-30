"""
🚀 AstroHealth AI — Single-File Gradio Deployment

Knowledge-Grounded & Explainable AI Framework
for Astronaut Health Monitoring and Performance Optimization.
"""

import json
import os
import re
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

# ==============================================================================
# 1. CONFIGURATION
# ==============================================================================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

AVAILABLE_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
]

DEFAULT_MODEL = "gpt-4o-mini"

APP_TITLE = "🚀 AstroHealth AI"
APP_SUBTITLE = "Knowledge-Grounded & Explainable AI for Astronaut Health Monitoring"
APP_ICON = "🧑‍🚀"

SYSTEM_PROMPT = """You are AstroHealth AI — a specialized, knowledge-grounded medical assistant \
for astronaut health monitoring and performance optimization aboard the International Space Station \
and deep-space missions.

ROLE & CONSTRAINTS:
• You ONLY answer questions related to astronaut health, space medicine, crew performance, \
  and related life-support topics.
• For unrelated queries, politely redirect the user to ask about astronaut health topics.
• Always ground your answers in the provided KNOWLEDGE CONTEXT when available.
• If the knowledge context is insufficient, say so honestly and provide your best reasoning.

RESPONSE FORMAT:
1. Provide a clear, structured answer with headings/bullets when appropriate.
2. After the main answer, include an EXPLAINABILITY BLOCK in the following JSON format \
   (enclosed in ```json ``` code fences):

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

SAMPLE_QUESTIONS = [
    "What are the main cardiovascular risks for astronauts during long-duration missions?",
    "How does microgravity affect bone density, and what countermeasures are used?",
    "Explain the SANS condition and its impact on astronaut vision.",
    "What exercise protocols are used on the ISS to maintain crew fitness?",
]


# ==============================================================================
# 2. KNOWLEDGE BASE
# ==============================================================================
KNOWLEDGE_BASE = [
    {
        "topic": "Cardiovascular Deconditioning",
        "keywords": ["cardiovascular", "heart", "blood pressure", "orthostatic", "cardiac", "deconditioning", "fluid shift", "blood volume", "arrhythmia", "vascular"],
        "content": "In microgravity, the cardiovascular system undergoes significant adaptation. Without gravitational pull, ~2 liters of fluid shifts from the lower body toward the head and thorax, causing facial puffiness and 'bird legs.' Cardiac output initially increases, but over weeks the heart undergoes mild atrophy (~8-10% reduction in left ventricular mass over 6 months). Blood volume decreases by ~10-15% as the body senses fluid overload and reduces plasma volume via diuresis.\n\nUpon return to Earth, astronauts commonly experience orthostatic intolerance — inability to maintain blood pressure when standing upright. Countermeasures include: (1) Lower Body Negative Pressure (LBNP) devices, (2) fluid loading protocols before re-entry (salt tablets + ~1L fluid), (3) regular aerobic exercise on the CEVIS cycle ergometer and T2 treadmill, (4) compression garments during re-entry. The Cardiovascular Health in Space (CVHS) program monitors continuous ECG, blood pressure, and echocardiography on the ISS.",
    },
    {
        "topic": "Bone Density Loss & Musculoskeletal Health",
        "keywords": ["bone", "density", "osteoporosis", "calcium", "musculoskeletal", "muscle atrophy", "sarcopenia", "ARED", "resistance exercise", "skeletal", "fracture"],
        "content": "Astronauts lose bone mineral density (BMD) at a rate of ~1-1.5% per month in weight-bearing bones (hip, spine, calcaneus), roughly 10× the rate of postmenopausal osteoporosis on Earth. Calcium is lost through urine, increasing the risk of renal stones. Muscle atrophy can reach 20% in postural muscles within 2 weeks without countermeasures.\n\nPrimary countermeasures:\n• Advanced Resistive Exercise Device (ARED): Provides up to 600 lbs of resistance, simulating squats, deadlifts, heel raises, and bench press in microgravity. Studies show ARED users maintain ~95% of pre-flight BMD.\n• Bisphosphonate therapy (alendronate) has been trialed to inhibit osteoclast activity.\n• Vitamin D supplementation (800-1000 IU/day) to compensate for lack of sunlight-driven synthesis.\n• Nutritional monitoring ensures adequate calcium (1000-1200 mg/day) and protein (0.8-1.2 g/kg/day) intake.\nRecovery post-flight can take 3-4 years for full BMD restoration in some cases.",
    },
    {
        "topic": "Space Radiation Exposure",
        "keywords": ["radiation", "cosmic rays", "GCR", "SPE", "solar particle", "dosimetry", "shielding", "cancer risk", "DNA damage", "radiation exposure", "sievert", "gray"],
        "content": "Astronauts face two main radiation sources: Galactic Cosmic Rays (GCR) — high-energy protons and heavy ions from outside the solar system, and Solar Particle Events (SPE) — bursts of energetic protons from solar flares and coronal mass ejections.\n\nOn the ISS (~400 km altitude), astronauts receive ~0.5-1.0 mSv/day, roughly 150-200 mSv over a 6-month mission — about 100× the annual ground-level dose. For a Mars mission (~3 years), cumulative dose could exceed 1 Sv, significantly increasing cancer risk.\n\nMonitoring: Crew Personal Dosimeters (CPD), Tissue Equivalent Proportional Counters (TEPC), and the ISS-RAD detector provide real-time exposure data. Biological dosimetry (chromosome aberration assays, γ-H2AX foci counting) quantifies DNA damage.\n\nCountermeasures: Polyethylene shielding (effective against SPE protons), storm shelters for SPE events, pharmacological radioprotectors (amifostine, antioxidant cocktails), and schedule optimization to limit EVA during high radiation periods. NASA's career dose limit is based on age and sex, capped at a 3% Risk of Exposure-Induced Death (REID).",
    },
    {
        "topic": "Sleep & Circadian Rhythm Disruption",
        "keywords": ["sleep", "circadian", "insomnia", "melatonin", "fatigue", "light therapy", "alertness", "rest", "sleep quality", "work schedule", "sleep deprivation"],
        "content": "On the ISS, astronauts experience 16 sunrises/sunsets per day (~90-minute orbital period), severely disrupting circadian rhythms. Average sleep duration in space is ~6.0-6.5 hours vs. the recommended 7-8 hours. Sleep quality is reduced due to noise (~60-70 dB ambient), microgravity discomfort, and psychological stress.\n\nMonitoring tools: Actigraphy wristbands track sleep-wake cycles, the Reaction Self Test (RST) measures psychomotor vigilance (equivalent to PVT on Earth), and periodic sleep diaries record subjective quality.\n\nCountermeasures:\n• Dynamic lighting system (2017+) with tunable LEDs: Blue-enriched light (~6500K) during wake periods for alertness; warm dimmed light (~2700K) before sleep to promote melatonin secretion.\n• Scheduled sleep-wake cycles (crew day: 06:00-21:30 GMT).\n• Melatonin supplements (0.3-3 mg) for circadian re-alignment.\n• Zolpidem and zaleplon available for acute insomnia (rarely used due to side effects).\n• Exercise timing optimization: Morning exercise improves nighttime sleep quality.",
    },
    {
        "topic": "Spaceflight Associated Neuro-ocular Syndrome (SANS)",
        "keywords": ["SANS", "vision", "ocular", "intracranial pressure", "optic disc", "papilledema", "eye", "neuro-ocular", "choroidal folds", "globe flattening", "ICP"],
        "content": "SANS (Spaceflight Associated Neuro-ocular Syndrome) is one of NASA's top health risks. It affects ~70% of long-duration ISS astronauts to some degree.\n\nPathophysiology: In microgravity, cephalad fluid shift increases intracranial pressure (ICP). Elevated ICP is transmitted along the optic nerve sheath, causing optic disc edema (papilledema), globe flattening, choroidal folds, and hyperopic refractive shifts (+0.50 to +1.75 diopters).\n\nDiagnosis: Fundoscopy, OCT (Optical Coherence Tomography) to measure retinal nerve fiber layer thickness, visual acuity testing, and tonometry (intraocular pressure measurement).\n\nCurrent monitoring on ISS: Fundoscope imaging, ultrasound of the optic nerve sheath diameter (ONSD), and the Visual Impairment Intracranial Pressure (VIIP) screening protocol.\n\nResearch countermeasures: Lower Body Negative Pressure (LBNP) to draw fluid caudally, thigh cuffs (venous occlusion), pharmacological ICP reduction (acetazolamide), and spacecraft design modifications for artificial gravity (centrifuge-based short-arm systems).",
    },
    {
        "topic": "Psychological Health & Behavioral Performance",
        "keywords": ["psychology", "mental health", "stress", "isolation", "depression", "anxiety", "crew dynamics", "behavioral", "morale", "teamwork", "conflict", "psychological", "loneliness"],
        "content": "Psychological health is critical for mission success. Key stressors include: confinement in a small habitat, isolation from family, communication delays (up to 24 min one-way for Mars), monotony, high workload, and interpersonal conflict in small crews.\n\nDocumented effects: The 'third-quarter phenomenon' — decreased morale at ~75% of mission duration. Asthenia/neurasthenia symptoms: irritability, emotional lability, fatigue, and cognitive slowing.\n\nMonitoring & Support:\n• Weekly private psychological conferences (WPC) with flight surgeons.\n• Behavioral Health & Performance (BHP) team provides continuous support.\n• Journals, mood questionnaires, and cognitive testing batteries.\n• Family video conferences, 'surprise' care packages, and personal items.\n\nCountermeasures:\n• Pre-flight: Antarctic analog missions (Concordia, McMurdo), team-building, cross-cultural training.\n• In-flight: Autonomy in scheduling, 'Earth-viewing' time, recreational activities, and peer support training.\n• Future: AI-based affect recognition systems, virtual reality nature environments, and autonomous behavioral health monitoring.",
    },
    {
        "topic": "Exercise Protocols & Physical Fitness",
        "keywords": ["exercise", "fitness", "CEVIS", "T2 treadmill", "ARED", "aerobic", "resistance training", "VO2 max", "workout", "physical performance", "endurance", "strength"],
        "content": "Astronauts on the ISS exercise ~2.5 hours per day (including setup/cleanup) to counteract microgravity deconditioning.\n\nEquipment:\n• CEVIS (Cycle Ergometer with Vibration Isolation & Stabilization): Aerobic cycling for cardiovascular conditioning. Astronauts perform interval and continuous protocols at 60-85% HRmax.\n• T2/COLBERT Treadmill: Running with a harness-bungee system providing ~70-80% body weight loading. Supports interval sprints and endurance running.\n• ARED (Advanced Resistive Exercise Device): Up to 600 lbs resistance via vacuum cylinders. Exercises include squats, deadlifts, heel raises, bench press, and upright rows.\n\nProtocol: Typical weekly schedule includes 6 days of exercise — alternating between aerobic (CEVIS/T2) and resistance (ARED) sessions.\n\nMonitoring: VO2max testing (periodic), heart-rate zones during sessions, subjective RPE (Rating of Perceived Exertion), and strength/power assessments using ARED force data. Post-flight functional fitness testing includes ladder climb, hatch opening simulation, and recovery walk.",
    },
    {
        "topic": "Nutrition & Hydration in Space",
        "keywords": ["nutrition", "diet", "food", "hydration", "calories", "vitamins", "supplements", "protein", "electrolytes", "water", "meal", "eating"],
        "content": "Nutritional requirements change in microgravity. NASA's ISS food system provides ~1800-3200 kcal/day based on crew member mass and activity level.\n\nKey nutritional concerns:\n• Iron overload: Red blood cell mass decreases in space, releasing iron. Excess iron increases oxidative stress. NASA limits iron intake to <10 mg/day.\n• Vitamin D deficiency: No UVB exposure in spacecraft. Supplementation of 800-1000 IU/day is mandatory.\n• Sodium restriction: High sodium accelerates bone loss and increases ICP. Target: <3500 mg/day (reduced from historical >5000 mg/day).\n• Omega-3 fatty acids (EPA/DHA): Shown to be osteoprotective and anti-inflammatory; supplementation is encouraged.\n• Folate and B-vitamins: Critical for DNA repair given radiation exposure.\n\nHydration: The ISS Water Recovery System (WRS) processes ~3.6 gallons/person/day from humidity condensate and urine. Crew members are encouraged to drink ~2-2.5 L/day. Dehydration monitoring via urine specific gravity and tracking daily intake logs.\n\nEmerging research: Personalized nutrition plans using metabolomics data, and biofortified crops from the Veggie and Advanced Plant Habitat growth chambers on the ISS.",
    },
    {
        "topic": "Immune System Changes in Space",
        "keywords": ["immune", "immunity", "infection", "virus", "herpes", "reactivation", "T-cell", "cytokine", "immune suppression", "bacteria", "microbiome", "white blood cell"],
        "content": "Spaceflight causes immune dysregulation through multiple mechanisms:\n\nObserved changes:\n• Latent virus reactivation: Epstein-Barr (EBV), Varicella-Zoster (VZV), and Cytomegalovirus (CMV) are reactivated in >50% of ISS crew, detectable via saliva PCR. Most reactivations are asymptomatic but indicate immune suppression.\n• T-cell function reduction: Decreased proliferation capacity and altered cytokine profiles (increased IL-6, decreased IL-2).\n• NK cell activity reduction: Diminished ability to kill tumor cells and virus-infected cells.\n• Altered microbiome: Shifts in gut and skin microbiota composition.\n\nContributing factors: Radiation exposure, stress hormones (cortisol), disrupted circadian rhythms, and altered nutrition.\n\nMonitoring: Pre/post-flight comprehensive immune panels, in-flight saliva collection for viral shedding analysis, and the Integrated Immune study.\n\nCountermeasures: Strict pre-flight quarantine (10-14 days), vaccination updates, probiotic supplementation research, and exercise (which partially mitigates immune suppression). Future pharmacological interventions are under study, including targeted immunomodulators.",
    },
    {
        "topic": "Performance Metrics & Crew Readiness",
        "keywords": ["performance", "cognitive", "readiness", "task performance", "reaction time", "workload", "efficiency", "crew", "productivity", "error rate", "decision making", "assessment"],
        "content": "Astronaut performance is multidimensional — encompassing physical fitness, cognitive function, and operational readiness.\n\nCognitive Performance Monitoring:\n• Cognition Test Battery: Includes spatial orientation, emotion recognition, abstract reasoning, risk decision-making, and psychomotor vigilance tests. Administered weekly on the ISS.\n• Reaction Self Test (RST): 3-minute psychomotor vigilance task measuring sustained attention — key for detecting fatigue-related impairment.\n\nPhysical Performance:\n• VO2max (aerobic capacity) — periodic testing on CEVIS.\n• Grip strength, functional reach, and timed obstacle course.\n• Post-flight Field Test: timed tasks simulating emergency egress — ladder climb, hatch opening, rock pickup, and suited walk.\n\nOperational Metrics:\n• Task completion rates and error frequency during complex procedures.\n• Communication effectiveness (measured via ground-crew interaction logs).\n• Crew coordination scores from peer evaluations.\n\nThe Integrated Medical Model (IMM) combines health data, environmental factors, and performance scores to estimate mission risk probability, supporting real-time go/no-go decisions for EVAs and critical operations.",
    }
]

def retrieve_relevant_knowledge(query: str, top_k: int = 3) -> list[dict]:
    query_lower = query.lower()
    query_words = set(query_lower.split())
    scored_entries = []
    
    for entry in KNOWLEDGE_BASE:
        score = 0
        for kw in entry["keywords"]:
            kw_lower = kw.lower()
            if kw_lower in query_lower:
                score += 3
            elif any(kw_lower in word or word in kw_lower for word in query_words):
                score += 1
        
        topic_lower = entry["topic"].lower()
        for word in query_words:
            if len(word) > 3 and word in topic_lower:
                score += 2

        if score > 0:
            scored_entries.append((score, entry))

    scored_entries.sort(key=lambda x: x[0], reverse=True)
    return [entry for _, entry in scored_entries[:top_k]]

def format_knowledge_context(entries: list[dict]) -> str:
    if not entries:
        return "No specific knowledge base entries matched this query. Use your general knowledge about space medicine."
    sections = [f"━━━ Source {i}: {entry['topic']} ━━━\n{entry['content']}" for i, entry in enumerate(entries, 1)]
    return "\n\n".join(sections)

def get_all_topics() -> list[str]:
    return [entry["topic"] for entry in KNOWLEDGE_BASE]


# ==============================================================================
# 3. EXPLAINABILITY ENGINE
# ==============================================================================
def parse_explainability(response_text: str) -> dict | None:
    pattern = r"```json\s*(\{.*?\})\s*```"
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
            
    pattern2 = r'\{\s*"confidence"\s*:.*?\}'
    match2 = re.search(pattern2, response_text, re.DOTALL)
    if match2:
        try:
            return json.loads(match2.group(0))
        except json.JSONDecodeError:
            pass
    return None

def extract_main_response(response_text: str) -> str:
    cleaned = re.sub(r"```json\s*\{.*?\}\s*```", "", response_text, flags=re.DOTALL).strip()
    return re.sub(r"[-─━=]{3,}\s*$", "", cleaned).strip()

def get_confidence_emoji(confidence: str) -> str:
    mapping = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}
    return mapping.get(confidence.upper(), "⚪")

def format_explainability_text(explain_data: dict) -> str:
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


# ==============================================================================
# 4. GRADIO INTERFACE
# ==============================================================================
def chat(message: str, history: list, api_key: str, model: str, temperature: float):
    key = api_key.strip() or OPENAI_API_KEY
    if not key:
        return (
            "⚠️ **Please enter your OpenAI API key** in the settings panel above to start chatting.",
            "No API key provided.",
        )

    relevant = retrieve_relevant_knowledge(message)
    context = format_knowledge_context(relevant)
    augmented_system = f"{SYSTEM_PROMPT}\n\n═══ KNOWLEDGE CONTEXT ═══\n{context}\n═══ END CONTEXT ═══"

    messages = [{"role": "system", "content": augmented_system}]
    for user_msg, bot_msg in (history or [])[-10:]:
        messages.append({"role": "user", "content": user_msg})
        if bot_msg:
            messages.append({"role": "assistant", "content": bot_msg})

    messages.append({"role": "user", "content": message})

    try:
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=2000,
        )
        full_response = response.choices[0].message.content
        explain = parse_explainability(full_response)
        main_answer = extract_main_response(full_response)
        explain_text = format_explainability_text(explain) if explain else "No explainability data in this response."
        return main_answer, explain_text
    except Exception as e:
        return f"❌ **Error:** {str(e)}", f"Error occurred: {str(e)}"

def create_gradio_app():
    custom_css = """
    .gradio-container { background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 40%, #0d1117 100%) !important; font-family: 'Inter', 'Segoe UI', sans-serif; }
    .main-title { text-align: center; padding: 1.2rem; background: linear-gradient(135deg, rgba(56,189,248,0.1), rgba(139,92,246,0.1)); border-radius: 16px; border: 1px solid rgba(56,189,248,0.2); margin-bottom: 1rem; }
    .main-title h1 { font-size: 2rem; background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; }
    .main-title p { color: #94a3b8; margin: 0.3rem 0 0; }
    .explain-box { background: rgba(15, 23, 42, 0.9) !important; border: 1px solid rgba(56, 189, 248, 0.3) !important; border-radius: 12px !important; font-family: 'Fira Code', 'Consolas', monospace !important; font-size: 0.85rem !important; }
    .topic-list { color: #c4b5fd; font-size: 0.85rem; line-height: 2; }
    footer { display: none !important; }
    """

    with gr.Blocks(title="AstroHealth AI", css=custom_css, theme=gr.themes.Base(primary_hue="sky", secondary_hue="violet", neutral_hue="slate").set(body_background_fill="*neutral_950", body_text_color="*neutral_200", block_background_fill="*neutral_900", block_border_color="*neutral_700", input_background_fill="*neutral_800", button_primary_background_fill="*primary_600", button_primary_text_color="white")) as app:
        gr.HTML('<div class="main-title"><h1>🚀 AstroHealth AI</h1></div>')
        with gr.Row():
            with gr.Column(scale=1, min_width=280):
                gr.Markdown("### ⚙️ Settings")
                api_key_input = gr.Textbox(label="🔑 OpenAI API Key", placeholder="sk-...", type="password", value=OPENAI_API_KEY or "")
                model_dropdown = gr.Dropdown(choices=AVAILABLE_MODELS, value=DEFAULT_MODEL, label="🤖 Model")
                temp_slider = gr.Slider(minimum=0.0, maximum=1.5, value=0.4, step=0.1, label="🌡️ Temperature")
                gr.Markdown("---")
                gr.Markdown("### 📚 Knowledge Topics")
                topics_text = "\n".join(f"• {t}" for t in get_all_topics())
                gr.Markdown(f'<div class="topic-list">{topics_text}</div>')
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(label="💬 Chat", height=450)
                with gr.Row():
                    msg_input = gr.Textbox(placeholder="Ask about astronaut health, performance, or space medicine...", label="Your Message", scale=5, show_label=False)
                    send_btn = gr.Button("🚀 Send", variant="primary", scale=1)
                with gr.Accordion("🔍 Explainability Details", open=False):
                    explain_output = gr.Textbox(label="", lines=12, interactive=False, elem_classes=["explain-box"])
                gr.Markdown("### 💡 Sample Questions")
                with gr.Row():
                    sample_btns = [(gr.Button(f"🔹 {q}", size="sm", variant="secondary"), q) for q in SAMPLE_QUESTIONS[:4]]

        chat_history_state = gr.State([])

        def respond(message, chat_history_internal, api_key, model, temperature):
            if not message.strip():
                return "", chat_history_internal, [], "Please enter a message."
            answer, explain_text = chat(message, chat_history_internal, api_key, model, temperature)
            chat_history_internal = chat_history_internal or []
            chat_history_internal.append((message, answer))
            display_messages = []
            for user_msg, bot_msg in chat_history_internal:
                display_messages.append({"role": "user", "content": user_msg})
                if bot_msg:
                    display_messages.append({"role": "assistant", "content": bot_msg})
            return "", chat_history_internal, display_messages, explain_text

        send_btn.click(respond, inputs=[msg_input, chat_history_state, api_key_input, model_dropdown, temp_slider], outputs=[msg_input, chat_history_state, chatbot, explain_output])
        msg_input.submit(respond, inputs=[msg_input, chat_history_state, api_key_input, model_dropdown, temp_slider], outputs=[msg_input, chat_history_state, chatbot, explain_output])
        
        for btn, question in sample_btns:
            btn.click(lambda q=question: q, outputs=[msg_input]).then(respond, inputs=[msg_input, chat_history_state, api_key_input, model_dropdown, temp_slider], outputs=[msg_input, chat_history_state, chatbot, explain_output])
            
    return app

if __name__ == "__main__":
    demo = create_gradio_app()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
