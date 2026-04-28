"""
ClarityBuddy — models.py
Pydantic request/response models for all API routes.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, List, Dict, Any


# ── Quiz Submission ──────────────────────────────────

class Quiz1Payload(BaseModel):
    name:   str = Field(..., min_length=1, max_length=100)
    email:  EmailStr
    answers: Dict[str, str] = Field(..., description="q1..q20 -> 'a'|'b'|'c'|'d'")


class Quiz2Payload(BaseModel):
    name:         str = Field(..., min_length=1, max_length=100)
    email:        EmailStr
    partner_name: Optional[str] = Field(None, max_length=100)
    answers:      Dict[str, str] = Field(..., description="eq1..fq2 -> 'a'|'b'|'c'|'d'")


class QuizResponse(BaseModel):
    report_id: str
    archetype: str
    score:     int


# ── Report ───────────────────────────────────────────

class ReportPreview(BaseModel):
    report_id: str
    archetype: str
    score:     int
    paid:      bool
    quiz_type: str


class FullReport(BaseModel):
    report_id:      str
    archetype:      str
    score:          int
    quiz_type:      str
    strengths:      str
    blind_spots:    str
    journal_prompts: List[str]
    next_step:      str
    # Quiz 2 extras
    dimensions:     Optional[Dict[str, int]] = None
    green_flags:    Optional[str] = None
    risk_zones:     Optional[str] = None
    decision:       Optional[str] = None


# ── Payment ──────────────────────────────────────────

PlanType = Literal['quiz1', 'quiz2', 'single', 'combo', 'monthly', 'annual']

class CreatePaymentPayload(BaseModel):
    report_id: str
    plan:      PlanType = 'single'


class CreatePaymentResponse(BaseModel):
    order_id: str
    amount:   int       # paise
    currency: str = 'INR'
    key_id:   str


class VerifyPaymentPayload(BaseModel):
    razorpay_order_id:   str
    razorpay_payment_id: str
    razorpay_signature:  str
    report_id:           str


class VerifyPaymentResponse(BaseModel):
    success: bool


# ── Coach ────────────────────────────────────────────

class ChatMessage(BaseModel):
    role:    Literal['user', 'assistant']
    content: str


class CoachChatPayload(BaseModel):
    report_id: str
    message:   str = Field(..., min_length=1, max_length=2000)
    history:   List[ChatMessage] = Field(default_factory=list)


class CoachChatResponse(BaseModel):
    reply: str
