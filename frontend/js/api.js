/* ═══════════════════════════════════════════════════
   ClarityBuddy — js/api.js
   All communication with the Python FastAPI backend.
   Backend URL is set via window.CB_API_URL
═══════════════════════════════════════════════════ */

const API_BASE = window.CB_API_URL || 'http://localhost:8000';

/* ── Internal fetch wrapper ── */
async function _request(method, path, body = null, timeoutMs = 60000) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);

  /* Use AbortController for timeout */
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  opts.signal = controller.signal;

  try {
    console.log(`[API] ${method} ${path} (timeout: ${timeoutMs}ms)`, body);
    const res = await fetch(`${API_BASE}${path}`, opts);
    const data = await res.json();
    console.log(`[API] Response: ${res.status}`, data);

    if (!res.ok) {
      const raw = data.detail || data.message || 'Something went wrong. Please try again.';
      const msg = typeof raw === 'string' ? raw : 'Something went wrong. Please try again.';
      console.error(`[API] Error ${res.status}:`, data);
      throw new Error(msg);
    }
    return data;
  } catch (err) {
    console.error(`[API] Fetch failed:`, err.message);
    throw err;
  } finally {
    clearTimeout(timeoutId);
  }
}

/* ─────────────────────────────────────────
   QUIZ 1 — Submit Self Reflection answers
   Returns: { report_id, archetype, score }
───────────────────────────────────────── */
export async function submitQuiz1(payload) {
  // payload: { name, email, answers: { q1: "a", q2: "b", ... } }
  // Increased timeout (90s) because OpenAI generation takes 10-15 seconds
  return _request('POST', '/api/submit-quiz1', payload, 90000);
}

/* ─────────────────────────────────────────
   QUIZ 2 — Submit Compatibility answers
   Returns: { report_id, score, dimensions }
───────────────────────────────────────── */
export async function submitQuiz2(payload) {
  // payload: { name, email, partner_name, answers: { q1: "a", ... } }
  // Increased timeout (90s) because OpenAI generation takes 10-15 seconds
  return _request('POST', '/api/submit-quiz2', payload, 90000);
}

/* ─────────────────────────────────────────
   REPORT — Get free preview
   Returns: { report_id, archetype, score, paid }
───────────────────────────────────────── */
export async function getReportPreview(reportId) {
  return _request('GET', `/api/report/${reportId}`);
}

/* ─────────────────────────────────────────
   REPORT — Get full report (paid)
   Returns: { full_report, archetype, score, ... }
───────────────────────────────────────── */
export async function getFullReport(reportId) {
  return _request('GET', `/api/report/${reportId}/full`);
}

/* ─────────────────────────────────────────
   PAYMENT — Create Razorpay order
   Returns: { order_id, amount, currency, key_id }
───────────────────────────────────────── */
export async function createPaymentOrder(payload) {
  // payload: { report_id, plan }
  // plan: 'single' | 'combo' | 'monthly' | 'annual'
  return _request('POST', '/api/create-payment', payload);
}

/* ─────────────────────────────────────────
   PAYMENT — Verify after Razorpay success
   Returns: { success: true }
───────────────────────────────────────── */
export async function verifyPayment(payload) {
  // payload: { razorpay_order_id, razorpay_payment_id, razorpay_signature, report_id }
  return _request('POST', '/api/verify-payment', payload);
}

/* ─────────────────────────────────────────
   COACH — Send chat message (subscribers)
   Returns: { reply: "..." }
───────────────────────────────────────── */
export async function sendCoachMessage(payload) {
  // payload: { report_id, message, history: [{role, content}] }
  return _request('POST', '/api/coach/chat', payload);
}
