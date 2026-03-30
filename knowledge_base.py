"""
Knowledge Base Module for Astronaut Health Monitoring Chatbot.

Contains curated domain knowledge about astronaut health, space medicine,
and performance optimization. Provides retrieval functions to ground
chatbot responses in verified facts.
"""

# ─── Domain Knowledge Corpus ────────────────────────────────────────
# Each entry: { "topic": ..., "keywords": [...], "content": ... }

KNOWLEDGE_BASE = [
    {
        "topic": "Cardiovascular Deconditioning",
        "keywords": [
            "cardiovascular", "heart", "blood pressure", "orthostatic",
            "cardiac", "deconditioning", "fluid shift", "blood volume",
            "arrhythmia", "vascular"
        ],
        "content": (
            "In microgravity, the cardiovascular system undergoes significant adaptation. "
            "Without gravitational pull, ~2 liters of fluid shifts from the lower body toward "
            "the head and thorax, causing facial puffiness and 'bird legs.' Cardiac output "
            "initially increases, but over weeks the heart undergoes mild atrophy (~8-10% "
            "reduction in left ventricular mass over 6 months). Blood volume decreases by "
            "~10-15% as the body senses fluid overload and reduces plasma volume via diuresis.\n\n"
            "Upon return to Earth, astronauts commonly experience orthostatic intolerance — "
            "inability to maintain blood pressure when standing upright. Countermeasures "
            "include: (1) Lower Body Negative Pressure (LBNP) devices, (2) fluid loading "
            "protocols before re-entry (salt tablets + ~1L fluid), (3) regular aerobic "
            "exercise on the CEVIS cycle ergometer and T2 treadmill, (4) compression garments "
            "during re-entry. The Cardiovascular Health in Space (CVHS) program monitors "
            "continuous ECG, blood pressure, and echocardiography on the ISS."
        ),
    },
    {
        "topic": "Bone Density Loss & Musculoskeletal Health",
        "keywords": [
            "bone", "density", "osteoporosis", "calcium", "musculoskeletal",
            "muscle atrophy", "sarcopenia", "ARED", "resistance exercise",
            "skeletal", "fracture"
        ],
        "content": (
            "Astronauts lose bone mineral density (BMD) at a rate of ~1-1.5% per month in "
            "weight-bearing bones (hip, spine, calcaneus), roughly 10× the rate of "
            "postmenopausal osteoporosis on Earth. Calcium is lost through urine, increasing "
            "the risk of renal stones. Muscle atrophy can reach 20% in postural muscles "
            "within 2 weeks without countermeasures.\n\n"
            "Primary countermeasures:\n"
            "• Advanced Resistive Exercise Device (ARED): Provides up to 600 lbs of "
            "resistance, simulating squats, deadlifts, heel raises, and bench press in "
            "microgravity. Studies show ARED users maintain ~95% of pre-flight BMD.\n"
            "• Bisphosphonate therapy (alendronate) has been trialed to inhibit osteoclast "
            "activity.\n"
            "• Vitamin D supplementation (800-1000 IU/day) to compensate for lack of "
            "sunlight-driven synthesis.\n"
            "• Nutritional monitoring ensures adequate calcium (1000-1200 mg/day) and "
            "protein (0.8-1.2 g/kg/day) intake.\n"
            "Recovery post-flight can take 3-4 years for full BMD restoration in some cases."
        ),
    },
    {
        "topic": "Space Radiation Exposure",
        "keywords": [
            "radiation", "cosmic rays", "GCR", "SPE", "solar particle",
            "dosimetry", "shielding", "cancer risk", "DNA damage",
            "radiation exposure", "sievert", "gray"
        ],
        "content": (
            "Astronauts face two main radiation sources: Galactic Cosmic Rays (GCR) — "
            "high-energy protons and heavy ions from outside the solar system, and Solar "
            "Particle Events (SPE) — bursts of energetic protons from solar flares and "
            "coronal mass ejections.\n\n"
            "On the ISS (~400 km altitude), astronauts receive ~0.5-1.0 mSv/day, roughly "
            "150-200 mSv over a 6-month mission — about 100× the annual ground-level dose. "
            "For a Mars mission (~3 years), cumulative dose could exceed 1 Sv, significantly "
            "increasing cancer risk.\n\n"
            "Monitoring: Crew Personal Dosimeters (CPD), Tissue Equivalent Proportional "
            "Counters (TEPC), and the ISS-RAD detector provide real-time exposure data. "
            "Biological dosimetry (chromosome aberration assays, γ-H2AX foci counting) "
            "quantifies DNA damage.\n\n"
            "Countermeasures: Polyethylene shielding (effective against SPE protons), "
            "storm shelters for SPE events, pharmacological radioprotectors (amifostine, "
            "antioxidant cocktails), and schedule optimization to limit EVA during high "
            "radiation periods. NASA's career dose limit is based on age and sex, capped "
            "at a 3% Risk of Exposure-Induced Death (REID)."
        ),
    },
    {
        "topic": "Sleep & Circadian Rhythm Disruption",
        "keywords": [
            "sleep", "circadian", "insomnia", "melatonin", "fatigue",
            "light therapy", "alertness", "rest", "sleep quality",
            "work schedule", "sleep deprivation"
        ],
        "content": (
            "On the ISS, astronauts experience 16 sunrises/sunsets per day (~90-minute "
            "orbital period), severely disrupting circadian rhythms. Average sleep duration "
            "in space is ~6.0-6.5 hours vs. the recommended 7-8 hours. Sleep quality is "
            "reduced due to noise (~60-70 dB ambient), microgravity discomfort, and "
            "psychological stress.\n\n"
            "Monitoring tools: Actigraphy wristbands track sleep-wake cycles, the Reaction "
            "Self Test (RST) measures psychomotor vigilance (equivalent to PVT on Earth), "
            "and periodic sleep diaries record subjective quality.\n\n"
            "Countermeasures:\n"
            "• Dynamic lighting system (2017+) with tunable LEDs: Blue-enriched light "
            "(~6500K) during wake periods for alertness; warm dimmed light (~2700K) before "
            "sleep to promote melatonin secretion.\n"
            "• Scheduled sleep-wake cycles (crew day: 06:00-21:30 GMT).\n"
            "• Melatonin supplements (0.3-3 mg) for circadian re-alignment.\n"
            "• Zolpidem and zaleplon available for acute insomnia (rarely used due to "
            "side effects).\n"
            "• Exercise timing optimization: Morning exercise improves nighttime sleep quality."
        ),
    },
    {
        "topic": "Spaceflight Associated Neuro-ocular Syndrome (SANS)",
        "keywords": [
            "SANS", "vision", "ocular", "intracranial pressure", "optic disc",
            "papilledema", "eye", "neuro-ocular", "choroidal folds",
            "globe flattening", "ICP"
        ],
        "content": (
            "SANS (Spaceflight Associated Neuro-ocular Syndrome) is one of NASA's top "
            "health risks. It affects ~70% of long-duration ISS astronauts to some degree.\n\n"
            "Pathophysiology: In microgravity, cephalad fluid shift increases intracranial "
            "pressure (ICP). Elevated ICP is transmitted along the optic nerve sheath, "
            "causing optic disc edema (papilledema), globe flattening, choroidal folds, "
            "and hyperopic refractive shifts (+0.50 to +1.75 diopters).\n\n"
            "Diagnosis: Fundoscopy, OCT (Optical Coherence Tomography) to measure retinal "
            "nerve fiber layer thickness, visual acuity testing, and tonometry (intraocular "
            "pressure measurement).\n\n"
            "Current monitoring on ISS: Fundoscope imaging, ultrasound of the optic nerve "
            "sheath diameter (ONSD), and the Visual Impairment Intracranial Pressure (VIIP) "
            "screening protocol.\n\n"
            "Research countermeasures: Lower Body Negative Pressure (LBNP) to draw fluid "
            "caudally, thigh cuffs (venous occlusion), pharmacological ICP reduction "
            "(acetazolamide), and spacecraft design modifications for artificial gravity "
            "(centrifuge-based short-arm systems)."
        ),
    },
    {
        "topic": "Psychological Health & Behavioral Performance",
        "keywords": [
            "psychology", "mental health", "stress", "isolation", "depression",
            "anxiety", "crew dynamics", "behavioral", "morale", "teamwork",
            "conflict", "psychological", "loneliness"
        ],
        "content": (
            "Psychological health is critical for mission success. Key stressors include: "
            "confinement in a small habitat, isolation from family, communication delays "
            "(up to 24 min one-way for Mars), monotony, high workload, and interpersonal "
            "conflict in small crews.\n\n"
            "Documented effects: The 'third-quarter phenomenon' — decreased morale at ~75% "
            "of mission duration. Asthenia/neurasthenia symptoms: irritability, emotional "
            "lability, fatigue, and cognitive slowing.\n\n"
            "Monitoring & Support:\n"
            "• Weekly private psychological conferences (WPC) with flight surgeons.\n"
            "• Behavioral Health & Performance (BHP) team provides continuous support.\n"
            "• Journals, mood questionnaires, and cognitive testing batteries.\n"
            "• Family video conferences, 'surprise' care packages, and personal items.\n\n"
            "Countermeasures:\n"
            "• Pre-flight: Antarctic analog missions (Concordia, McMurdo), team-building, "
            "cross-cultural training.\n"
            "• In-flight: Autonomy in scheduling, 'Earth-viewing' time, recreational "
            "activities, and peer support training.\n"
            "• Future: AI-based affect recognition systems, virtual reality nature "
            "environments, and autonomous behavioral health monitoring."
        ),
    },
    {
        "topic": "Exercise Protocols & Physical Fitness",
        "keywords": [
            "exercise", "fitness", "CEVIS", "T2 treadmill", "ARED",
            "aerobic", "resistance training", "VO2 max", "workout",
            "physical performance", "endurance", "strength"
        ],
        "content": (
            "Astronauts on the ISS exercise ~2.5 hours per day (including setup/cleanup) "
            "to counteract microgravity deconditioning.\n\n"
            "Equipment:\n"
            "• CEVIS (Cycle Ergometer with Vibration Isolation & Stabilization): Aerobic "
            "cycling for cardiovascular conditioning. Astronauts perform interval and "
            "continuous protocols at 60-85% HRmax.\n"
            "• T2/COLBERT Treadmill: Running with a harness-bungee system providing ~70-80% "
            "body weight loading. Supports interval sprints and endurance running.\n"
            "• ARED (Advanced Resistive Exercise Device): Up to 600 lbs resistance via "
            "vacuum cylinders. Exercises include squats, deadlifts, heel raises, bench "
            "press, and upright rows.\n\n"
            "Protocol: Typical weekly schedule includes 6 days of exercise — alternating "
            "between aerobic (CEVIS/T2) and resistance (ARED) sessions.\n\n"
            "Monitoring: VO2max testing (periodic), heart-rate zones during sessions, "
            "subjective RPE (Rating of Perceived Exertion), and strength/power assessments "
            "using ARED force data. Post-flight functional fitness testing includes "
            "ladder climb, hatch opening simulation, and recovery walk."
        ),
    },
    {
        "topic": "Nutrition & Hydration in Space",
        "keywords": [
            "nutrition", "diet", "food", "hydration", "calories",
            "vitamins", "supplements", "protein", "electrolytes",
            "water", "meal", "eating"
        ],
        "content": (
            "Nutritional requirements change in microgravity. NASA's ISS food system "
            "provides ~1800-3200 kcal/day based on crew member mass and activity level.\n\n"
            "Key nutritional concerns:\n"
            "• Iron overload: Red blood cell mass decreases in space, releasing iron. "
            "Excess iron increases oxidative stress. NASA limits iron intake to <10 mg/day.\n"
            "• Vitamin D deficiency: No UVB exposure in spacecraft. Supplementation of "
            "800-1000 IU/day is mandatory.\n"
            "• Sodium restriction: High sodium accelerates bone loss and increases ICP. "
            "Target: <3500 mg/day (reduced from historical >5000 mg/day).\n"
            "• Omega-3 fatty acids (EPA/DHA): Shown to be osteoprotective and "
            "anti-inflammatory; supplementation is encouraged.\n"
            "• Folate and B-vitamins: Critical for DNA repair given radiation exposure.\n\n"
            "Hydration: The ISS Water Recovery System (WRS) processes ~3.6 gallons/person/day "
            "from humidity condensate and urine. Crew members are encouraged to drink "
            "~2-2.5 L/day. Dehydration monitoring via urine specific gravity and tracking "
            "daily intake logs.\n\n"
            "Emerging research: Personalized nutrition plans using metabolomics data, "
            "and biofortified crops from the Veggie and Advanced Plant Habitat growth "
            "chambers on the ISS."
        ),
    },
    {
        "topic": "Immune System Changes in Space",
        "keywords": [
            "immune", "immunity", "infection", "virus", "herpes",
            "reactivation", "T-cell", "cytokine", "immune suppression",
            "bacteria", "microbiome", "white blood cell"
        ],
        "content": (
            "Spaceflight causes immune dysregulation through multiple mechanisms:\n\n"
            "Observed changes:\n"
            "• Latent virus reactivation: Epstein-Barr (EBV), Varicella-Zoster (VZV), "
            "and Cytomegalovirus (CMV) are reactivated in >50% of ISS crew, detectable "
            "via saliva PCR. Most reactivations are asymptomatic but indicate immune "
            "suppression.\n"
            "• T-cell function reduction: Decreased proliferation capacity and altered "
            "cytokine profiles (increased IL-6, decreased IL-2).\n"
            "• NK cell activity reduction: Diminished ability to kill tumor cells and "
            "virus-infected cells.\n"
            "• Altered microbiome: Shifts in gut and skin microbiota composition.\n\n"
            "Contributing factors: Radiation exposure, stress hormones (cortisol), "
            "disrupted circadian rhythms, and altered nutrition.\n\n"
            "Monitoring: Pre/post-flight comprehensive immune panels, in-flight saliva "
            "collection for viral shedding analysis, and the Integrated Immune study.\n\n"
            "Countermeasures: Strict pre-flight quarantine (10-14 days), vaccination "
            "updates, probiotic supplementation research, and exercise (which partially "
            "mitigates immune suppression). Future pharmacological interventions are under "
            "study, including targeted immunomodulators."
        ),
    },
    {
        "topic": "Performance Metrics & Crew Readiness",
        "keywords": [
            "performance", "cognitive", "readiness", "task performance",
            "reaction time", "workload", "efficiency", "crew",
            "productivity", "error rate", "decision making", "assessment"
        ],
        "content": (
            "Astronaut performance is multidimensional — encompassing physical fitness, "
            "cognitive function, and operational readiness.\n\n"
            "Cognitive Performance Monitoring:\n"
            "• Cognition Test Battery: Includes spatial orientation, emotion recognition, "
            "abstract reasoning, risk decision-making, and psychomotor vigilance tests. "
            "Administered weekly on the ISS.\n"
            "• Reaction Self Test (RST): 3-minute psychomotor vigilance task measuring "
            "sustained attention — key for detecting fatigue-related impairment.\n\n"
            "Physical Performance:\n"
            "• VO2max (aerobic capacity) — periodic testing on CEVIS.\n"
            "• Grip strength, functional reach, and timed obstacle course.\n"
            "• Post-flight Field Test: timed tasks simulating emergency egress — ladder "
            "climb, hatch opening, rock pickup, and suited walk.\n\n"
            "Operational Metrics:\n"
            "• Task completion rates and error frequency during complex procedures.\n"
            "• Communication effectiveness (measured via ground-crew interaction logs).\n"
            "• Crew coordination scores from peer evaluations.\n\n"
            "The Integrated Medical Model (IMM) combines health data, environmental "
            "factors, and performance scores to estimate mission risk probability, "
            "supporting real-time go/no-go decisions for EVAs and critical operations."
        ),
    },
]


# ─── Knowledge Retrieval Function ───────────────────────────────────

def retrieve_relevant_knowledge(query: str, top_k: int = 3) -> list[dict]:
    """
    Retrieves the most relevant knowledge entries for a given user query.
    Uses keyword matching with scoring (a simple but effective approach).
    
    Args:
        query: The user's question or message.
        top_k: Number of top matching entries to return.
    
    Returns:
        List of matching knowledge entries, sorted by relevance score.
    """
    query_lower = query.lower()
    query_words = set(query_lower.split())

    scored_entries = []
    for entry in KNOWLEDGE_BASE:
        score = 0
        # Check keyword matches
        for kw in entry["keywords"]:
            kw_lower = kw.lower()
            if kw_lower in query_lower:
                score += 3  # Exact substring match
            elif any(kw_lower in word or word in kw_lower for word in query_words):
                score += 1  # Partial word match

        # Check topic match
        topic_lower = entry["topic"].lower()
        for word in query_words:
            if len(word) > 3 and word in topic_lower:
                score += 2

        if score > 0:
            scored_entries.append((score, entry))

    # Sort by score descending, return top_k
    scored_entries.sort(key=lambda x: x[0], reverse=True)
    return [entry for _, entry in scored_entries[:top_k]]


def format_knowledge_context(entries: list[dict]) -> str:
    """
    Formats retrieved knowledge entries into a context string
    for injection into the LLM prompt.
    """
    if not entries:
        return "No specific knowledge base entries matched this query. Use your general knowledge about space medicine."

    sections = []
    for i, entry in enumerate(entries, 1):
        sections.append(
            f"━━━ Source {i}: {entry['topic']} ━━━\n{entry['content']}"
        )
    return "\n\n".join(sections)


def get_all_topics() -> list[str]:
    """Returns a list of all knowledge base topics."""
    return [entry["topic"] for entry in KNOWLEDGE_BASE]
