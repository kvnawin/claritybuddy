"""
ClarityBuddy — razorpay_service.py
Payment order creation and webhook signature verification.
"""

import os
import hmac
import hashlib
import razorpay

# Prices in paise (INR × 100)
PLAN_PRICES = {
    "single":  29900,
    "combo":   49900,
    "monthly": 39900,
    "annual":  299900,
}

def _client() -> razorpay.Client:
    key_id     = os.getenv("RAZORPAY_KEY_ID")
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")
    if not key_id or not key_secret:
        raise RuntimeError("RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET must be set")
    return razorpay.Client(auth=(key_id, key_secret))


def create_order(report_id: str, plan: str) -> dict:
    """
    Create a Razorpay order for a one-time payment.
    Returns: { order_id, amount, currency, key_id }
    """
    amount = PLAN_PRICES.get(plan, PLAN_PRICES["single"])
    rz     = _client()

    order = rz.order.create({
        "amount":   amount,
        "currency": "INR",
        "receipt":  f"cb_{report_id[:8]}",
        "notes": {
            "report_id": report_id,
            "plan":      plan,
        },
    })

    return {
        "order_id": order["id"],
        "amount":   amount,
        "currency": "INR",
        "key_id":   os.getenv("RAZORPAY_KEY_ID"),
    }


def verify_payment_signature(
    order_id:   str,
    payment_id: str,
    signature:  str,
) -> bool:
    """
    Verify Razorpay payment signature.
    Formula: HMAC-SHA256(order_id + "|" + payment_id, secret)
    """
    secret  = os.getenv("RAZORPAY_KEY_SECRET", "").encode()
    message = f"{order_id}|{payment_id}".encode()
    digest  = hmac.new(secret, message, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)


def verify_webhook_signature(payload_body: bytes, signature: str) -> bool:
    """
    Verify Razorpay webhook signature.
    Uses RAZORPAY_WEBHOOK_SECRET (separate from key secret).
    """
    secret  = os.getenv("RAZORPAY_WEBHOOK_SECRET", "").encode()
    digest  = hmac.new(secret, payload_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)
