"""
ClarityBuddy — openai_service.py
Builds GPT prompts, calls OpenAI, parses structured report.
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, Any, List
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

_client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=50.0,  # 50s timeout for OpenAI API calls
)

MODEL = "gpt-4o-mini"

# ── Load system prompts from files ──────────────────────

def _load_prompt(filename: str) -> str:
    path = Path(__file__).parent / "prompts" / filename
    return path.read_text(encoding="utf-8")


# ── Quiz 1: Generate Self Reflection Report ─────────────

async def generate_quiz1_report(
    name: str,
    answers: Dict[str, str],
) -> Dict[str, Any]:
    """
    Returns: {
      archetype, score, raw_text,
      strengths, blind_spots, journal_prompts, next_step
    }
    """
    logger.info(f"[OpenAI] Generating Quiz1 report for {name}")
    
    system_prompt = _load_prompt("quiz1_system.txt")
    logger.info(f"[OpenAI] Loaded system prompt: {len(system_prompt)} chars")
    
    user_message  = _build_quiz1_user_message(name, answers)
    logger.info(f"[OpenAI] Built user message: {len(user_message)} chars")

    logger.info(f"[OpenAI] Calling OpenAI API with model={MODEL}...")
    response = await _client.chat.completions.create(
        model=MODEL,
        max_tokens=1800,
        temperature=0.75,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
    )

    raw_text = response.choices[0].message.content.strip()
    logger.info(f"[OpenAI] Received response: {len(raw_text)} chars")
    logger.info(f"[OpenAI] Raw start: {raw_text[:400]!r}")

    result = _parse_quiz1_report(raw_text)
    logger.info(f"[OpenAI] Parsed report: archetype={result.get('archetype')}, score={result.get('score')}")
    
    return result


def _build_quiz1_user_message(name: str, answers: Dict[str, str]) -> str:
    QUESTION_MAP = {
        "q1":  "Non-negotiables in a relationship",
        "q2":  "Identity outside relationships",
        "q3":  "Response when someone violates values",
        "q4":  "Core values in a relationship",
        "q5":  "Clarity on non-negotiables",
        "q6":  "Reaction when a stable man shows interest",
        "q7":  "How much past hurt affects present decisions",
        "q8":  "How it feels to be in a relationship right now",
        "q9":  "Trust in own judgement",
        "q10": "Response to family/society pressure",
        "q11": "Type of men attracted to",
        "q12": "Emotional experience in past relationships",
        "q13": "What you did when relationship was wrong",
        "q14": "Role taken in relationships",
        "q15": "Which fear feels most familiar",
        "q16": "Ideal communication style",
        "q17": "Lifestyle description",
        "q18": "Emotional closeness preference",
        "q19": "What matters most for long-term future",
        "q20": "How ideal relationship in 5 years feels",
    }
    OPTION_MAP = {
        "q1":  {"a": "Confident — knows exactly what she needs", "b": "Somewhat clear", "c": "Confused — keeps changing her mind", "d": "Pressured — focuses on others' expectations"},
        "q2":  {"a": "Strong independent identity", "b": "Still figuring out who she is", "c": "Defines herself through others", "d": "Knows herself but doesn't trust it"},
        "q3":  {"a": "Walks away immediately", "b": "Gives another chance hoping they'll change", "c": "Stays but feels resentful", "d": "Questions whether standards are too high"},
        "q4":  {"a": "Emotional safety, honesty, respect", "b": "Stability, ambition, shared goals", "c": "Freedom, independence, personal space", "d": "Family, loyalty, traditional structure"},
        "q5":  {"a": "Clear written or mental list", "b": "Vague idea, not defined", "c": "Struggles to separate standards from fear", "d": "Compromises everything under pressure"},
        "q6":  {"a": "Excited and open", "b": "Slightly anxious but interested", "c": "Suspicious or doubtful", "d": "Numb or avoidant"},
        "q7":  {"a": "Very little — processed and healed", "b": "Some — certain triggers still catch her", "c": "Quite a lot — compares to past", "d": "Completely — hasn't dealt with it"},
        "q8":  {"a": "Genuinely wants and is ready", "b": "Appealing but scary", "c": "Overwhelming or too complicated", "d": "Escaping loneliness"},
        "q9":  {"a": "Yes, fully", "b": "Mostly, with some doubt", "c": "Not really — second-guesses everything", "d": "No — too many past mistakes"},
        "q10": {"a": "Stays grounded in own pace", "b": "Feels conflicted but manages it", "c": "Lets it significantly influence decisions", "d": "Makes choices primarily because of pressure"},
        "q11": {"a": "Emotionally mature and consistent", "b": "Charming but inconsistent", "c": "Emotionally unavailable or closed off", "d": "Caring but overly dependent"},
        "q12": {"a": "Calm, valued, and understood", "b": "Anxious, seeking reassurance", "c": "Confused about where she stood", "d": "Working harder than them"},
        "q13": {"a": "Walked away relatively quickly", "b": "Stayed hoping things would improve", "c": "Stayed from fear of being alone", "d": "Stayed from outside pressure"},
        "q14": {"a": "Equal partner — mutual effort", "b": "The healer or fixer", "c": "The one who adjusts and accommodates", "d": "The chaser — always initiating"},
        "q15": {"a": "Fear of losing independence", "b": "Fear of choosing wrong", "c": "Fear of being alone or too late", "d": "Fear of repeating past mistakes"},
        "q16": {"a": "Daily meaningful check-ins", "b": "Regular contact with personal space", "c": "Mostly independent with periodic deep conversations", "d": "Spontaneous — no fixed structure"},
        "q17": {"a": "Structured and routine-oriented", "b": "Balanced — mix of routine and flexibility", "c": "Spontaneous and social", "d": "Calm, introverted, homebody"},
        "q18": {"a": "Deep intimacy — sharing everything", "b": "Warm connection with healthy space", "c": "Gradual closeness — slow to open up", "d": "Independent connection — space is important"},
        "q19": {"a": "Emotional peace and stability", "b": "Growth and ambition together", "c": "Family orientation and rootedness", "d": "Freedom and personal fulfilment"},
        "q20": {"a": "Clear — knows exactly what she wants", "b": "Somewhat formed — still defining details", "c": "Vague — avoids thinking far ahead", "d": "Pressured — focuses on timeline more than vision"},
    }
    lines = [f"Name: {name}\n"]
    for qid, label in QUESTION_MAP.items():
        ans_key  = answers.get(qid, "")
        ans_text = OPTION_MAP.get(qid, {}).get(ans_key, ans_key)
        lines.append(f"Q{qid[1:]}: {label}\nAnswer: {ans_text}")
    return "\n".join(lines)


def _quiz1_section_key(upper: str):
    """Map a line to a section key, tolerating singular/plural and markdown decoration."""
    if "CLARITY PERSONA" in upper or "YOUR PERSONA" in upper:
        return "archetype"
    if "YOUR STRENGTH" in upper:          # covers "YOUR STRENGTHS" and "YOUR STRENGTH"
        return "strengths"
    if "BLIND SPOT" in upper:             # covers "YOUR BLIND SPOTS" and "BLIND SPOT"
        return "blind_spots"
    if "CLARITY SCORE" in upper:
        return "score"
    if "JOURNAL PROMPT" in upper:         # covers "YOUR JOURNAL PROMPTS" and "JOURNAL PROMPT"
        return "journal_prompts"
    if "NEXT STEP" in upper:
        return "next_step"
    return None


def _parse_quiz1_report(raw: str) -> Dict[str, Any]:
    sections = {}
    current  = None
    buffer   = []

    for line in raw.splitlines():
        stripped = line.strip()
        upper    = stripped.upper()
        key      = _quiz1_section_key(upper)

        if key is not None:
            _flush(sections, current, buffer)
            current = key
            if key == "score":
                # Capture inline score, e.g. "YOUR CLARITY SCORE: 72/100"
                pos  = upper.find("CLARITY SCORE") + len("CLARITY SCORE")
                tail = stripped[pos:].strip(' :-—–')
                buffer = [tail] if tail else []
            else:
                buffer = []
        elif current:
            buffer.append(stripped)

    _flush(sections, current, buffer)
    logger.info(f"[Parser] quiz1 sections found: { {k: bool(v) for k, v in sections.items()} }")

    # Extract archetype name
    arch_text = sections.get("archetype", "")
    archetype = _extract_archetype(arch_text)

    # Extract score number
    score_text = sections.get("score", "")
    score      = _extract_score(score_text)
    # Fallback: if section was empty, search the full raw text for X/100
    if not score_text:
        m = re.search(r'(\d{2,3})\s*/\s*100\b', raw)
        if m:
            val = int(m.group(1))
            if 1 <= val <= 100:
                score = val

    # Parse journal prompts as list
    prompts_text = sections.get("journal_prompts", "")
    prompts      = _extract_prompts(prompts_text)

    return {
        "archetype":       archetype,
        "score":           score,
        "raw_text":        raw,
        "strengths":       sections.get("strengths", ""),
        "blind_spots":     sections.get("blind_spots", ""),
        "journal_prompts": prompts,
        "next_step":       sections.get("next_step", ""),
    }


# ── Quiz 2: Generate Compatibility Report ───────────────

async def generate_quiz2_report(
    name:         str,
    partner_name: str,
    answers:      Dict[str, str],
) -> Dict[str, Any]:
    system_prompt = _load_prompt("quiz2_system.txt")
    user_message  = _build_quiz2_user_message(name, partner_name, answers)

    response = await _client.chat.completions.create(
        model=MODEL,
        max_tokens=1800,
        temperature=0.75,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
    )

    raw_text = response.choices[0].message.content.strip()
    return _parse_quiz2_report(raw_text)


def _build_quiz2_user_message(name: str, partner_name: str, answers: Dict[str, str]) -> str:
    DIMENSION_MAP = {
        "eq1":     "Emotional — his response when she's upset",
        "eq2":     "Emotional — day-to-day emotional availability",
        "cq1":     "Communication — what happens when they disagree",
        "cq2":     "Communication — comfort expressing real needs",
        "lq1":     "Lifestyle — alignment of day-to-day lives",
        "lq2":     "Lifestyle — individual space and independence",
        "vq1":     "Values — honesty and integrity",
        "vq2":     "Values — core values around family and commitment",
        "gq1":     "Growth — support for her personal goals",
        "gq2":     "Growth — his direction in life",
        "fq1":     "Future Vision — conversations about the future",
        "fq2":     "Future Vision — imagining life with him in 5 years",
        "overall": "Overall emotional experience in the relationship",
    }
    lines = [f"Her name: {name}\nHis name: {partner_name or 'partner'}\n"]
    for qid, label in DIMENSION_MAP.items():
        ans = answers.get(qid, "a")
        lines.append(f"{label}\nAnswer: Option {ans.upper()}")
    return "\n".join(lines)


def _parse_quiz2_report(raw: str) -> Dict[str, Any]:
    sections = {}
    current  = None
    buffer   = []

    for line in raw.splitlines():
        stripped = line.strip()
        upper    = stripped.upper()

        if "COMPATIBILITY SCORE" in upper or "OVERALL SCORE" in upper:
            _flush(sections, current, buffer); current = "score"
            header_key = "COMPATIBILITY SCORE" if "COMPATIBILITY SCORE" in upper else "OVERALL SCORE"
            tail = stripped[upper.find(header_key) + len(header_key):].strip(' :-—–')
            buffer = [tail] if tail else []
        elif "DIMENSION SCORE" in upper or "DIMENSION BREAKDOWN" in upper or "DIMENSION ANALYSIS" in upper:
            _flush(sections, current, buffer); current = "dimensions_raw"; buffer = []
        elif "GREEN FLAG" in upper:       # covers "GREEN FLAGS" and "GREEN FLAG"
            _flush(sections, current, buffer); current = "green_flags"; buffer = []
        elif "RISK ZONE" in upper or "CAUTION" in upper or "CONCERN" in upper:
            _flush(sections, current, buffer); current = "risk_zones"; buffer = []
        elif "MOVE FORWARD" in upper or "DECISION" in upper or "STEP BACK" in upper or "RECOMMENDATION" in upper:
            _flush(sections, current, buffer); current = "decision"; buffer = []
        elif "JOURNAL PROMPT" in upper:   # covers "JOURNAL PROMPTS" and "JOURNAL PROMPT"
            _flush(sections, current, buffer); current = "journal_prompts"; buffer = []
        elif current:
            buffer.append(stripped)

    _flush(sections, current, buffer)
    logger.info(f"[Parser] quiz2 sections found: { {k: bool(v) for k, v in sections.items()} }")

    score_text = sections.get("score", "")
    score      = _extract_score(score_text, max_score=60)
    # Fallback: if section was empty, search full raw text for X/60
    if not score_text:
        m = re.search(r'(\d{1,2})\s*/\s*60\b', raw)
        if m:
            val = int(m.group(1))
            if 1 <= val <= 60:
                score = val
    prompts    = _extract_prompts(sections.get("journal_prompts", ""))
    dimensions = _extract_dimensions(sections.get("dimensions_raw", ""))

    return {
        "archetype":       f"Compatibility Score: {score}/60",
        "score":           score,
        "raw_text":        raw,
        "strengths":       sections.get("green_flags", ""),
        "blind_spots":     sections.get("risk_zones", ""),
        "journal_prompts": prompts,
        "next_step":       sections.get("decision", ""),
        "dimensions":      dimensions,
        "green_flags":     sections.get("green_flags", ""),
        "risk_zones":      sections.get("risk_zones", ""),
        "decision":        sections.get("decision", ""),
    }


# ── Quiz 3: Generate Relationship Clarity Report ────────────

_CONTRADICTION_LABELS = {
    'desires_safety_but_attracted_inconsistency': 'Consciously desires emotional safety but may still feel emotionally drawn to inconsistency and unpredictability',
    'low_trust_high_overthinking':               'Tends to over-analyse excessively when her intuition has already signalled a concern',
    'pressure_driven_not_ready':                 'Part of the urgency around relationships appears to come from external pressure rather than genuine emotional readiness',
    'knows_values_cant_enforce_boundaries':      'Intellectually clear on what she values but struggles to enforce those boundaries when emotionally attached',
    'blind_spots_with_self_trust':               'Shows self-trust in general but has notable blind spots when emotionally attracted to someone',
    'avoidant_but_wants_commitment':             'Consciously desires commitment but emotionally distances herself as intimacy deepens',
}

_SCORE_LABELS = {
    (80, 100): 'Strong',
    (60,  79): 'Moderate',
    (40,  59): 'Developing',
    ( 0,  39): 'Low',
}

def _score_label(s: int) -> str:
    for (lo, hi), label in _SCORE_LABELS.items():
        if lo <= s <= hi:
            return label
    return 'Moderate'

_RISK_LABELS = {
    (70, 100): 'High Risk',
    (40,  69): 'Moderate',
    ( 0,  39): 'Low Risk',
}

def _risk_label(s: int) -> str:
    for (lo, hi), label in _RISK_LABELS.items():
        if lo <= s <= hi:
            return label
    return 'Moderate'


async def generate_quiz3_report(
    name:    str,
    scores:  Dict[str, Any],
    derived: Dict[str, Any],
) -> Dict[str, Any]:
    logger.info(f"[OpenAI] Generating Quiz3 report for {name}")
    system_prompt = _load_prompt("quiz3_system.txt")
    user_message  = _build_quiz3_user_message(name, scores, derived)

    response = await _client.chat.completions.create(
        model=MODEL,
        max_tokens=2200,
        temperature=0.75,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
    )

    raw_text = response.choices[0].message.content.strip()
    logger.info(f"[OpenAI] Quiz3 response: {len(raw_text)} chars")
    return _parse_quiz3_report(raw_text, derived, scores)


def _build_quiz3_user_message(name: str, scores: Dict[str, Any], derived: Dict[str, Any]) -> str:
    s = scores
    overall = derived.get('overallScore', 0)
    attachment = derived.get('attachmentStyle', '')
    mrt = derived.get('marriageReadinessType', '')
    patterns = derived.get('dominantPatterns', [])
    contradictions = derived.get('contradictions', [])

    lines = [
        f"Name: {name}",
        "",
        f"OVERALL CLARITY SCORE: {overall}/100",
        "",
        "━━━ DIMENSION SCORES ━━━",
        "",
        f"Identity Clarity: {s.get('identityClarity',0)}/100 — {_score_label(s.get('identityClarity',0))} self-awareness and value clarity",
        f"Emotional Stability: {s.get('emotionalStability',0)}/100 — {_score_label(s.get('emotionalStability',0))} emotional regulation and grounding",
        f"Boundary Strength: {s.get('boundaryStrength',0)}/100 — {_score_label(s.get('boundaryStrength',0))} boundary enforcement and self-respect",
        f"Pressure Vulnerability: {s.get('pressureVulnerability',0)}/100 — {_risk_label(s.get('pressureVulnerability',0))} influence from external/timeline pressure",
        f"Self-Trust: {s.get('selfTrust',0)}/100 — {_score_label(s.get('selfTrust',0))} trust in own intuition and judgement",
        f"Secure Attachment Tendency: {s.get('secureAttachment',0)}/100",
        f"Anxious Attachment Tendency: {s.get('anxiousAttachment',0)}/100",
        f"Avoidant Attachment Tendency: {s.get('avoidantAttachment',0)}/100",
        f"Fearful-Avoidant Tendency: {s.get('fearfulAvoidant',0)}/100",
        f"Red Flag Blindness Risk: {s.get('redFlagBlindness',0)}/100 — {_risk_label(s.get('redFlagBlindness',0))} tendency to rationalise concerning behaviour",
        f"Overthinking Risk: {s.get('overthinking',0)}/100 — {_risk_label(s.get('overthinking',0))} mental looping and analysis",
        f"Intuition Trust: {s.get('intuitionTrust',0)}/100 — {_score_label(s.get('intuitionTrust',0))} trust in intuitive signals",
        f"\"Good On Paper\" Bias: {s.get('goodOnPaperBias',0)}/100 — {_risk_label(s.get('goodOnPaperBias',0))} checklist-driven attraction",
        f"Emotional Availability Mismatch: {s.get('emotionalAvailabilityMismatch',0)}/100 — {_risk_label(s.get('emotionalAvailabilityMismatch',0))} attraction toward emotionally unavailable types",
        f"Marriage Readiness: {s.get('marriageReadiness',0)}/100 — {_score_label(s.get('marriageReadiness',0))}",
        "",
        "━━━ DERIVED PROFILE ━━━",
        "",
        f"Attachment Style: {attachment}",
        f"Marriage Readiness Type: {mrt}",
        f"Top 3 Dominant Patterns: {' · '.join(patterns) if patterns else 'Not determined'}",
    ]

    if contradictions:
        lines += ["", "━━━ DETECTED CONTRADICTIONS ━━━", ""]
        for i, c in enumerate(contradictions[:3], 1):
            label = _CONTRADICTION_LABELS.get(c, c.replace('_', ' ').capitalize())
            lines.append(f"{i}. {label}")

    lines += [
        "",
        "Generate the complete Relationship Clarity Report following the exact section structure and formatting instructions.",
        "The scorecard section must use the exact dimension scores provided above.",
    ]

    return "\n".join(lines)


_Q3_SECTION_MAP = {
    "YOUR RELATIONSHIP CLARITY PROFILE":  "clarityProfile",
    "YOUR STRONGEST PATTERNS":            "strongestPatterns",
    "YOUR HIDDEN BLIND SPOTS":            "hiddenBlindSpots",
    "WHAT MAY BE CAUSING YOUR CONFUSION": "confusion",
    "YOUR RELATIONSHIP DECISION STYLE":   "decisionStyle",
    "YOUR EMOTIONAL PATTERN IN LOVE":     "emotionalPattern",
    "YOUR BIGGEST GROWTH EDGE":           "growthEdge",
    "YOUR PERSONAL CLARITY SCORECARD":    "scorecard",
    "YOUR JOURNAL PROMPTS":               "journalPrompts",
    "YOUR NEXT STEP":                     "nextStep",
}

def _quiz3_section_key(line: str):
    """Exact-match section headers after stripping markdown/decorators.
    Substring matching caused body sentences to trigger false header detection."""
    if len(line) > 60:
        return None
    # Strip *, #, _, -, =, spaces and common GPT decorators
    import re as _re
    cleaned = _re.sub(r'[^A-Z\s]', '', line.upper()).strip()
    return _Q3_SECTION_MAP.get(cleaned)


def _parse_quiz3_report(raw: str, derived: Dict[str, Any], scores: Dict[str, Any] = None) -> Dict[str, Any]:
    sections: Dict[str, str] = {}
    current  = None
    buffer   = []

    for line in raw.splitlines():
        stripped = line.strip()
        upper    = stripped.upper()
        key      = _quiz3_section_key(upper)

        if key is not None:
            _flush(sections, current, buffer)
            current = key
            buffer  = []
        elif current:
            buffer.append(stripped)

    _flush(sections, current, buffer)
    logger.info(f"[Parser] quiz3 sections found: { {k: bool(v) for k, v in sections.items()} }")

    prompts  = _extract_prompts(sections.get("journalPrompts", ""))
    next_step = sections.get("nextStep", "")
    dominant_pattern = (derived.get("dominantPatterns") or ["Clarity Seeker"])[0]

    return {
        "dominant_pattern":        dominant_pattern,
        "overall_score":           derived.get("overallScore", 0),
        "attachment_style":        derived.get("attachmentStyle", ""),
        "marriage_readiness_type": derived.get("marriageReadinessType", ""),
        "dominant_patterns":       derived.get("dominantPatterns", []),
        "raw_text":                raw,
        "strengths":               sections.get("strongestPatterns", ""),
        "blind_spots":             sections.get("hiddenBlindSpots", ""),
        "journal_prompts":         prompts,
        "next_step":               next_step,
        "dimensions": {
            "attachmentStyle":        derived.get("attachmentStyle", ""),
            "marriageReadinessType":  derived.get("marriageReadinessType", ""),
            "dominantPatterns":       derived.get("dominantPatterns", []),
            "overallScore":           derived.get("overallScore", 0),
            "scores":                 scores or {},
            "sections": {
                "clarityProfile":   sections.get("clarityProfile", ""),
                "confusion":        sections.get("confusion", ""),
                "decisionStyle":    sections.get("decisionStyle", ""),
                "emotionalPattern": sections.get("emotionalPattern", ""),
                "growthEdge":       sections.get("growthEdge", ""),
                "scorecard":        sections.get("scorecard", ""),
            }
        },
    }


# ── AI Clarity Coach ─────────────────────────────────────

async def coach_reply(
    system_prompt: str,
    history:       List[Dict[str, str]],
    user_message:  str,
) -> str:
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history[-10:]:  # last 10 turns for context
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    response = await _client.chat.completions.create(
        model=MODEL,
        max_tokens=500,
        temperature=0.8,
        messages=messages,
    )
    return response.choices[0].message.content.strip()


def build_coach_system_prompt(report: Dict[str, Any]) -> str:
    """Inject user's stored data into the coach system prompt template."""
    template = _load_prompt("coach_system.txt")
    return (
        template
        .replace("{user_name}",          report.get("name", ""))
        .replace("{user_persona}",        report.get("archetype", ""))
        .replace("{clarity_score}",      str(report.get("score", "")))
        .replace("{quiz_date}",          str(report.get("created_at", ""))[:10])
        .replace("{fear_answer}",        report.get("answers", {}).get("q15", ""))
        .replace("{readiness_answer}",   report.get("answers", {}).get("q8", ""))
        .replace("{pattern_answer}",     report.get("answers", {}).get("q14", ""))
        .replace("{blindspot_from_report}", report.get("blind_spots", "")[:300])
        .replace("{strength_from_report}",  report.get("strengths", "")[:300])
    )


# ── Helpers ─────────────────────────────────────────────

def _flush(d: dict, key: str, buf: list) -> None:
    if key:
        d[key] = "\n".join(buf).strip()

def _extract_archetype(text: str) -> str:
    archetypes = [
        "The Careful Heart",
        "The Devoted Giver",
        "The Deep Thinker",
        "The Dutiful Heart",
        "The Free Spirit",
        "The Romantic Believer",
        "The Grounded Chooser",
    ]
    for a in archetypes:
        if a.lower() in text.lower():
            return a
    return "The Deep Thinker"  # safe default

def _extract_score(text: str, max_score: int = 100) -> int:
    # Prefer "X/max_score" pattern — prevents grabbing the denominator first
    match = re.search(rf'(\d{{1,3}})\s*/{max_score}\b', text)
    if match:
        val = int(match.group(1))
        if 1 <= val <= max_score:
            return val
    # Fallback: first 2-3 digit number within range
    nums = re.findall(r'\b(\d{2,3})\b', text)
    for n in nums:
        val = int(n)
        if 1 <= val <= max_score:
            return val
    return max_score // 2  # neutral default, not the maximum

def _extract_prompts(text: str) -> List[str]:
    lines = [l.strip().lstrip("•-0123456789. ") for l in text.splitlines() if l.strip()]
    lines = [l for l in lines if len(l) > 20]
    return lines[:5]

def _extract_dimensions(text: str) -> Dict[str, int]:
    dims = {}
    KEYS = ["emotional", "communication", "lifestyle", "values", "growth", "future"]
    for line in text.splitlines():
        for key in KEYS:
            if key in line.lower():
                nums = re.findall(r'\b(\d+)\b', line)
                if nums:
                    dims[key] = min(int(nums[0]), 10)
    return dims
