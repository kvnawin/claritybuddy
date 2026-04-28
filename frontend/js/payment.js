/* ═══════════════════════════════════════════════════
   ClarityBuddy — js/payment.js
   Handles Razorpay checkout flow.
   Loaded on report.html after free preview shown.
═══════════════════════════════════════════════════ */

import { createPaymentOrder, verifyPayment } from './api.js';

/* Plans config — matches backend pricing */
export const PLANS = {
  quiz1:   { label: 'Self Reflection Report', price: 19900,  desc: 'Full AI report — Quiz 1' },
  quiz2:   { label: 'Compatibility Report',   price: 29900,  desc: 'Full AI report — Quiz 2' },
  single:  { label: 'Single Report',          price: 19900,  desc: 'Full AI report for this quiz' },
  combo:   { label: 'Combo Report',           price: 49900,  desc: 'Both Quiz 1 + Quiz 2 reports' },
  monthly: { label: 'Monthly Plan',           price: 39900,  desc: 'Unlimited coach + retake every 90 days' },
  annual:  { label: 'Annual Plan',            price: 299900, desc: 'Full year — clarity as a practice' },
};

/* ─────────────────────────────────────────
   openCheckout(reportId, plan)
   Loads Razorpay script if needed,
   creates order via backend, opens modal.
───────────────────────────────────────── */
export async function openCheckout(reportId, plan = 'single', userInfo = {}) {
  /* ensure Razorpay script is loaded */
  await _loadRazorpayScript();

  const btn = document.getElementById('btn-unlock');
  if (btn) { btn.classList.add('btn--loading'); btn.disabled = true; }

  try {
    const order = await createPaymentOrder({ report_id: reportId, plan });

    const options = {
      key:         order.key_id,
      amount:      order.amount,
      currency:    order.currency || 'INR',
      name:        'ClarityBuddy',
      description: PLANS[plan]?.label || 'Report Unlock',
      order_id:    order.order_id,
      prefill: {
        name:  userInfo.name  || '',
        email: userInfo.email || '',
      },
      theme: { color: '#C0644A' },
      modal: {
        ondismiss: () => {
          if (btn) { btn.classList.remove('btn--loading'); btn.disabled = false; }
        },
      },
      handler: async (response) => {
        await _onPaymentSuccess(response, reportId);
      },
    };

    const rzp = new window.Razorpay(options);
    rzp.open();
  } catch (err) {
    if (btn) { btn.classList.remove('btn--loading'); btn.disabled = false; }
    _showError(err.message || 'Could not open payment. Please try again.');
  }
}

/* ── Payment success handler ── */
async function _onPaymentSuccess(response, reportId) {
  try {
    await verifyPayment({
      razorpay_order_id:   response.razorpay_order_id,
      razorpay_payment_id: response.razorpay_payment_id,
      razorpay_signature:  response.razorpay_signature,
      report_id:           reportId,
    });

    /* store payment id */
    localStorage.setItem('cb_payment_id', response.razorpay_payment_id);

    /* redirect to full report */
    window.location.href = `report.html?id=${reportId}&unlocked=1`;
  } catch (err) {
    _showError('Payment was received but we had trouble confirming it. Please contact support.');
  }
}

/* ── Load Razorpay SDK lazily ── */
function _loadRazorpayScript() {
  return new Promise((resolve, reject) => {
    if (window.Razorpay) { resolve(); return; }
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.onload  = resolve;
    script.onerror = () => reject(new Error('Could not load payment SDK. Check your connection.'));
    document.head.appendChild(script);
  });
}

function _showError(msg) {
  let toast = document.getElementById('cb-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'cb-toast';
    toast.className = 'toast toast--error';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 4000);
}
