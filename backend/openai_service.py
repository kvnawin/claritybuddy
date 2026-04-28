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


def _parse_quiz1_report(raw: str) -> Dict[str, Any]:
    """
    Expects the report to contain these section headers:
    YOUR CLARITY PERSONA, YOUR STRENGTHS, YOUR BLIND SPOTS,
    YOUR CLARITY SCORE, YOUR JOURNAL PROMPTS, YOUR NEXT STEP
    """
    sections = {}
    current  = None
    buffer   = []

    for line in raw.splitlines():
        stripped = line.strip()
        upper    = stripped.upper()

        if "YOUR CLARITY PERSONA" in upper:
            current = "archetype"; buffer = []
        elif "YOUR STRENGTHS" in upper:
            _flush(sections, current, buffer); current = "strengths"; buffer = []
        elif "YOUR BLIND SPOTS" in upper:
            _flush(sections, current, buffer); current = "blind_spots"; buffer = []
        elif "YOUR CLARITY SCORE" in upper:
            _flush(sections, current, buffer); current = "score"; buffer = []
        elif "YOUR JOURNAL PROMPTS" in upper:
            _flush(sections, current, buffer); current = "journal_prompts"; buffer = []
        elif "YOUR NEXT STEP" in upper:
            _flush(sections, current, buffer); current = "next_step"; buffer = []
        elif current:
            buffer.append(stripped)

    _flush(sections, current, buffer)

    # Extract archetype name
    arch_text = sections.get("archetype", "")
    archetype = _extract_archetype(arch_text)

    # Extract score number
    score_text = sections.get("score", "")
    score      = _extract_score(score_text)

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
            current = "score"; buffer = []
        elif "DIMENSION SCORES" in upper or "DIMENSION BREAKDOWN" in upper:
            _flush(sections, current, buffer); current = "dimensions_raw"; buffer = []
        elif "GREEN FLAGS" in upper:
            _flush(sections, current, buffer); current = "green_flags"; buffer = []
        elif "RISK ZONES" in upper or "CAUTION" in upper:
            _flush(sections, current, buffer); current = "risk_zones"; buffer = []
        elif "MOVE FORWARD" in upper or "DECISION" in upper or "STEP BACK" in upper:
            _flush(sections, current, buffer); current = "decision"; buffer = []
        elif "JOURNAL PROMPTS" in upper:
            _flush(sections, current, buffer); current = "journal_prompts"; buffer = []
        elif current:
            buffer.append(stripped)

    _flush(sections, current, buffer)

    score      = _extract_score(sections.get("score", ""), max_score=60)
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
        .replace("{user_archetype}",     report.get("archetype", ""))
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
        "The Guarded Protector",
        "The Hopeful Healer",
        "The Clarity Seeker",
        "The Pressure Pleaser",
        "The Grounded Chooser",
    ]
    for a in archetypes:
        if a.lower() in text.lower():
            return a
    return "The Clarity Seeker"  # safe default

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
