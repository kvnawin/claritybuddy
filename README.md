# ClarityBuddy

AI-powered relationship clarity app for Indian women (25–45). Based on the Relationship Clarity Workbook framework.

---

## Stack

| Layer | Service | Cost |
|---|---|---|
| Frontend | Vercel | Free |
| Backend | Railway | ~₹500/mo |
| Database | Supabase | Free tier |
| AI | OpenAI GPT-4o-mini | ~₹0.80/report |
| Payments | Razorpay | 2% per transaction |

---

## Local Development

### 1. Clone and set up environment

```bash
git clone https://github.com/yourname/claritybuddy.git
cd claritybuddy

# Backend
cd backend
cp .env.example .env
# Fill in your keys in .env
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Set your backend URL in all HTML files

In `frontend/quiz.html`, `frontend/compatibility.html`, `frontend/report.html`:

```js
window.CB_API_URL = 'http://localhost:8000';  // local dev
// change to Railway URL before deploying
```

### 3. Open frontend

Open `frontend/index.html` directly in browser, or use Live Server in VS Code.

---

## Supabase Setup

1. Create a project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor → New Query**
3. Paste and run the contents of `supabase_schema.sql`
4. Copy your **Project URL** and **service_role key** into `.env`

---

## Deploy Backend → Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select the `backend/` folder as root
4. Add all env vars from `.env` in Railway dashboard:
   - `OPENAI_API_KEY`
   - `RAZORPAY_KEY_ID`
   - `RAZORPAY_KEY_SECRET`
   - `RAZORPAY_WEBHOOK_SECRET`
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_KEY`
   - `FRONTEND_URL` = your Vercel URL
5. Railway auto-deploys from `railway.json`

---

## Deploy Frontend → Vercel

1. Go to [vercel.com](https://vercel.com) → New Project → Import from GitHub
2. Set **Root Directory** to `frontend/`
3. Deploy — Vercel detects static HTML automatically

---

## Razorpay Webhook

In Razorpay dashboard → Settings → Webhooks → Add:

```
URL: https://your-railway-url.railway.app/api/webhook/razorpay
Secret: (create one, add to RAZORPAY_WEBHOOK_SECRET env var)
Events: ✅ payment.captured  ✅ subscription.activated  ✅ subscription.charged
```

---

## Before Going Live

- [ ] Run `supabase_schema.sql` in Supabase
- [ ] Set all env vars in Railway dashboard
- [ ] Update `window.CB_API_URL` in all HTML files to Railway production URL
- [ ] Set `FRONTEND_URL` in Railway to Vercel production URL
- [ ] Add Razorpay webhook URL
- [ ] Test full flow: quiz → GPT → report preview → payment → full report
- [ ] Switch Razorpay from test mode to live mode

---

## File Structure

```
claritybuddy/
├── CLAUDE.md                  ← Claude Code memory
├── .gitignore
├── .env.example
├── supabase_schema.sql
├── README.md
├── frontend/
│   ├── index.html             ← Landing page
│   ├── quiz.html              ← Quiz 1 (20 questions)
│   ├── compatibility.html     ← Quiz 2 (15 questions)
│   ├── report.html            ← Free preview + paywall + full report
│   ├── thankyou.html          ← Post-payment confirmation
│   ├── css/main.css           ← All styles
│   ├── js/api.js              ← Backend API calls
│   ├── js/quiz.js             ← Quiz navigation engine
│   ├── js/payment.js          ← Razorpay integration
│   └── vercel.json
└── backend/
    ├── main.py                ← FastAPI routes
    ├── openai_service.py      ← GPT prompts + parsing
    ├── razorpay_service.py    ← Payment + webhook
    ├── database.py            ← Supabase operations
    ├── models.py              ← Pydantic models
    ├── requirements.txt
    ├── railway.json
    ├── .env.example
    └── prompts/
        ├── quiz1_system.txt   ← Self Reflection GPT prompt
        ├── quiz2_system.txt   ← Compatibility GPT prompt
        └── coach_system.txt   ← AI Clarity Coach prompt
```
