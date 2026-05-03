"""
ClarityBuddy — main.py
FastAPI application. All API routes.
Run locally: uvicorn main:app --reload --port 8000
"""

import os
import json
import logging
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from models import (
    Quiz1Payload, Quiz2Payload, QuizResponse,
    ReportPreview, FullReport,
    Quiz3Payload, Quiz3Response, Report3Preview, Report3Full,
    CreatePaymentPayload, CreatePaymentResponse,
    VerifyPaymentPayload, VerifyPaymentResponse,
    CoachChatPayload, CoachChatResponse,
)
import database as db
import openai_service as ai
import razorpay_service as rz

# ── App setup ────────────────────────────────────────────

app = FastAPI(
    title="ClarityBuddy API",
    version="1.0.0",
    docs_url="/docs",        # disable in production: docs_url=None
)

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5500")
DEV_MODE     = os.getenv("DEV_MODE", "false").lower() == "true"
if DEV_MODE:
    logger.warning("⚠️  DEV_MODE is ON — payment check bypassed. Never enable this in production.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "https://claritybuddy.in",
        "https://www.claritybuddy.in",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=False,
)

# ── Health check ─────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "service": "claritybuddy-api"}


# ═══════════════════════════════════════════════════
# QUIZ ROUTES
# ═══════════════════════════════════════════════════

@app.post("/api/submit-quiz1", response_model=QuizResponse)
async def submit_quiz1(payload: Quiz1Payload):
    """
    Receive Quiz 1 answers → call GPT → save report → return preview data.
    Takes ~10-15 seconds (GPT generation time).
    """
    logger.info(f"[API] POST /api/submit-quiz1 from {payload.email}")
    
    # 1. Create DB row first (so we have an ID)
    logger.info(f"[API] Creating DB report record...")
    report_id = db.create_report(
        email=payload.email,
        name=payload.name,
        quiz_type="quiz1",
        answers=payload.answers,
    )
    logger.info(f"[API] Created report: {report_id}")

    try:
        # 2. Generate report via GPT
        logger.info(f"[API] Calling OpenAI service...")
        result = await ai.generate_quiz1_report(
            name=payload.name,
            answers=payload.answers,
        )
        logger.info(f"[API] OpenAI returned: {result}")

        # 3. Save result to DB
        logger.info(f"[API] Saving report result to DB...")
        db.save_report_result(
            report_id=report_id,
            archetype=result["archetype"],
            score=result["score"],
            full_report_raw=result["raw_text"],
            parsed=result,
        )
        logger.info(f"[API] Report saved successfully")

        return QuizResponse(
            report_id=report_id,
            archetype=result["archetype"],
            score=result["score"],
        )

    except Exception as e:
        # Log the actual error for debugging
        logger.error(f"Quiz 1 generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Report generation failed. Please try again.")


@app.post("/api/submit-quiz2", response_model=QuizResponse)
async def submit_quiz2(payload: Quiz2Payload):
    """Receive Quiz 2 answers → call GPT → save report → return preview data."""
    report_id = db.create_report(
        email=payload.email,
        name=payload.name,
        quiz_type="quiz2",
        answers=payload.answers,
        partner_name=payload.partner_name,
    )

    try:
        result = await ai.generate_quiz2_report(
            name=payload.name,
            partner_name=payload.partner_name or "your partner",
            answers=payload.answers,
        )

        db.save_report_result(
            report_id=report_id,
            archetype=result["archetype"],
            score=result["score"],
            full_report_raw=result["raw_text"],
            parsed=result,
        )

        return QuizResponse(
            report_id=report_id,
            archetype=result["archetype"],
            score=result["score"],
        )

    except Exception as e:
        logger.error(f"Quiz 2 generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Report generation failed. Please try again.")


# ═══════════════════════════════════════════════════
# REPORT ROUTES
# ═══════════════════════════════════════════════════

@app.get("/api/report/{report_id}", response_model=ReportPreview)
async def get_report_preview(report_id: str):
    """Return archetype + score (always free). Also returns paid status."""
    report = db.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")

    return ReportPreview(
        report_id=report["id"],
        archetype=report.get("archetype", ""),
        score=report.get("score", 0),
        paid=report.get("paid", False),
        quiz_type=report.get("quiz_type", "quiz1"),
    )


@app.get("/api/report/{report_id}/full", response_model=FullReport)
async def get_full_report(report_id: str):
    """Return full report. Requires paid=true in DB."""
    report = db.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")
    if not DEV_MODE and not report.get("paid"):
        raise HTTPException(status_code=402, detail="Payment required to access full report.")

    return FullReport(
        report_id=report["id"],
        archetype=report.get("archetype", ""),
        score=report.get("score", 0),
        quiz_type=report.get("quiz_type", "quiz1"),
        strengths=report.get("strengths", ""),
        blind_spots=report.get("blind_spots", ""),
        journal_prompts=report.get("journal_prompts", []),
        next_step=report.get("next_step", ""),
        dimensions=report.get("dimensions"),
        green_flags=report.get("green_flags"),
        risk_zones=report.get("risk_zones"),
        decision=report.get("decision"),
    )


@app.post("/api/submit-quiz3", response_model=Quiz3Response)
async def submit_quiz3(payload: Quiz3Payload):
    """
    Receive Quiz 3 answers + pre-computed scores → call GPT → save → return preview data.
    Scores are computed client-side; GPT generates narrative interpretation only.
    """
    logger.info(f"[API] POST /api/submit-quiz3 from {payload.email}")

    report_id = db.create_report(
        email=payload.email,
        name=payload.name,
        quiz_type="quiz3",
        answers=payload.answers,
    )

    try:
        result = await ai.generate_quiz3_report(
            name=payload.name,
            scores=payload.scores,
            derived=payload.derived,
        )

        db.save_report_result(
            report_id=report_id,
            archetype=result["dominant_pattern"],
            score=result["overall_score"],
            full_report_raw=result["raw_text"],
            parsed=result,
        )

        return Quiz3Response(
            report_id=report_id,
            overall_score=result["overall_score"],
            attachment_style=result["attachment_style"],
            marriage_readiness_type=result["marriage_readiness_type"],
            dominant_patterns=result["dominant_patterns"],
        )

    except Exception as e:
        logger.error(f"Quiz 3 generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Report generation failed. Please try again.")


@app.get("/api/report3/{report_id}", response_model=Report3Preview)
async def get_report3_preview(report_id: str):
    """Return quiz3 scores + labels (always free). Also returns paid status."""
    report = db.get_report(report_id)
    if not report or report.get("quiz_type") != "quiz3":
        raise HTTPException(status_code=404, detail="Report not found.")

    dims = report.get("dimensions") or {}
    return Report3Preview(
        report_id=report["id"],
        overall_score=dims.get("overallScore", report.get("score", 0)),
        attachment_style=dims.get("attachmentStyle", ""),
        marriage_readiness_type=dims.get("marriageReadinessType", ""),
        dominant_patterns=dims.get("dominantPatterns", []),
        scores=dims.get("scores", {}),
        paid=report.get("paid", False),
    )


@app.get("/api/report3/{report_id}/full", response_model=Report3Full)
async def get_report3_full(report_id: str):
    """Return full quiz3 report. Requires paid=true in DB."""
    report = db.get_report(report_id)
    if not report or report.get("quiz_type") != "quiz3":
        raise HTTPException(status_code=404, detail="Report not found.")
    if not DEV_MODE and not report.get("paid"):
        raise HTTPException(status_code=402, detail="Payment required to access full report.")

    dims = report.get("dimensions") or {}
    sections = dims.get("sections", {})
    sections["strongestPatterns"] = report.get("strengths", "")
    sections["hiddenBlindSpots"]  = report.get("blind_spots", "")

    return Report3Full(
        report_id=report["id"],
        overall_score=dims.get("overallScore", report.get("score", 0)),
        attachment_style=dims.get("attachmentStyle", ""),
        marriage_readiness_type=dims.get("marriageReadinessType", ""),
        dominant_patterns=dims.get("dominantPatterns", []),
        scores=dims.get("scores", {}),
        sections=sections,
        journal_prompts=report.get("journal_prompts", []),
        next_step=report.get("next_step", ""),
        paid=report.get("paid", False),
    )


# ═══════════════════════════════════════════════════
# PAYMENT ROUTES
# ═══════════════════════════════════════════════════

@app.post("/api/create-payment", response_model=CreatePaymentResponse)
async def create_payment(payload: CreatePaymentPayload):
    """Create a Razorpay order. Returns order details for the frontend checkout."""
    report = db.get_report(payload.report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")
    if report.get("paid"):
        raise HTTPException(status_code=400, detail="This report is already unlocked.")

    try:
        order = rz.create_order(payload.report_id, payload.plan)
        return CreatePaymentResponse(**order)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not create payment order.")


@app.post("/api/verify-payment", response_model=VerifyPaymentResponse)
async def verify_payment(payload: VerifyPaymentPayload):
    """
    Verify Razorpay signature after frontend payment success.
    Marks report as paid in DB.
    """
    valid = rz.verify_payment_signature(
        order_id=payload.razorpay_order_id,
        payment_id=payload.razorpay_payment_id,
        signature=payload.razorpay_signature,
    )
    if not valid:
        raise HTTPException(status_code=400, detail="Payment signature verification failed.")

    db.mark_report_paid(payload.report_id, payload.razorpay_payment_id)
    return VerifyPaymentResponse(success=True)


@app.post("/api/webhook/razorpay")
async def razorpay_webhook(request: Request):
    """
    Razorpay calls this endpoint after payment events.
    Handles: payment.captured, subscription.activated, subscription.charged
    Configure in Razorpay dashboard → Webhooks.
    """
    body      = await request.body()
    signature = request.headers.get("x-razorpay-signature", "")

    if not rz.verify_webhook_signature(body, signature):
        raise HTTPException(status_code=400, detail="Invalid webhook signature.")

    event = json.loads(body)
    event_type = event.get("event")

    if event_type == "payment.captured":
        payment = event["payload"]["payment"]["entity"]
        notes   = payment.get("notes", {})
        report_id = notes.get("report_id")
        if report_id:
            db.mark_report_paid(report_id, payment["id"])

    elif event_type in ("subscription.activated", "subscription.charged"):
        sub     = event["payload"]["subscription"]["entity"]
        email   = sub.get("email") or sub.get("notes", {}).get("email", "")
        plan    = sub.get("notes", {}).get("plan", "monthly")
        sub_id  = sub.get("id", "")
        if email:
            db.create_or_update_subscription(email, plan, sub_id)

    return JSONResponse({"status": "ok"})


# ═══════════════════════════════════════════════════
# AI CLARITY COACH (Subscription only)
# ═══════════════════════════════════════════════════

@app.post("/api/coach/chat", response_model=CoachChatResponse)
async def coach_chat(payload: CoachChatPayload):
    """
    AI Clarity Coach chat endpoint.
    Requires active subscription. Uses user's stored report data
    to personalise every response.
    """
    # 1. Load report (has archetype, answers, etc.)
    report = db.get_report(payload.report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")

    # 2. Check subscription
    email = report.get("email", "")
    subscription = db.get_subscription(email)
    if not subscription:
        raise HTTPException(
            status_code=403,
            detail="Active subscription required to use the Clarity Coach."
        )

    # 3. Build personalised system prompt from their data
    system_prompt = ai.build_coach_system_prompt(report)

    # 4. Call GPT
    try:
        reply = await ai.coach_reply(
            system_prompt=system_prompt,
            history=[msg.dict() for msg in payload.history],
            user_message=payload.message,
        )
        return CoachChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Coach is unavailable. Please try again.")