"""
ClarityBuddy — database.py
Supabase client wrapper. All DB read/write operations live here.
"""

import os
import uuid
from typing import Optional, Dict, Any
from supabase import create_client, Client


def _client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
    return create_client(url, key)


# ── Create a new report row (before GPT runs) ───────────

def create_report(
    email:        str,
    name:         str,
    quiz_type:    str,
    answers:      Dict[str, str],
    partner_name: Optional[str] = None,
) -> str:
    """Insert a new report row, return the generated UUID."""
    report_id = str(uuid.uuid4())
    _client().table("reports").insert({
        "id":           report_id,
        "email":        email,
        "name":         name,
        "quiz_type":    quiz_type,
        "answers":      answers,
        "partner_name": partner_name,
        "paid":         False,
    }).execute()
    return report_id


# ── Save GPT output back to the report row ───────────────

def save_report_result(
    report_id:       str,
    archetype:       str,
    score:           int,
    full_report_raw: str,          # raw GPT text
    parsed:          Dict[str, Any],
) -> None:
    """Write archetype, score, and parsed sections to DB."""
    _client().table("reports").update({
        "archetype":       archetype,
        "score":           score,
        "full_report":     full_report_raw,
        "strengths":       parsed.get("strengths", ""),
        "blind_spots":     parsed.get("blind_spots", ""),
        "journal_prompts": parsed.get("journal_prompts", []),
        "next_step":       parsed.get("next_step", ""),
        # Quiz 2 fields
        "dimensions":      parsed.get("dimensions"),
        "green_flags":     parsed.get("green_flags"),
        "risk_zones":      parsed.get("risk_zones"),
        "decision":        parsed.get("decision"),
    }).eq("id", report_id).execute()


# ── Get report by id ─────────────────────────────────────

def get_report(report_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a report row. Returns None if not found."""
    res = _client().table("reports").select("*").eq("id", report_id).single().execute()
    return res.data if res.data else None


# ── Mark report as paid ──────────────────────────────────

def mark_report_paid(report_id: str, payment_id: str) -> None:
    _client().table("reports").update({
        "paid":       True,
        "payment_id": payment_id,
    }).eq("id", report_id).execute()


# ── Check subscription status ────────────────────────────

def get_subscription(email: str) -> Optional[Dict[str, Any]]:
    """
    Returns active subscription row or None.
    Table: subscriptions(id, email, plan, status, expires_at, razorpay_subscription_id)
    """
    res = (
        _client()
        .table("subscriptions")
        .select("*")
        .eq("email", email)
        .eq("status", "active")
        .single()
        .execute()
    )
    return res.data if res.data else None


def create_or_update_subscription(email: str, plan: str, razorpay_sub_id: str) -> None:
    """Upsert subscription row on activation."""
    _client().table("subscriptions").upsert({
        "email":                    email,
        "plan":                     plan,
        "status":                   "active",
        "razorpay_subscription_id": razorpay_sub_id,
    }).execute()
