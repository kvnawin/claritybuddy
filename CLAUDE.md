# ClarityBuddy — Claude Code Memory File
> Read this file fully before every session. Update it when decisions change.

---

## WHAT THIS PROJECT IS

ClarityBuddy is an AI-powered relationship clarity web app for unmarried Indian women (25–45).
Users take a quiz, get a personalised AI-generated report, and pay to unlock the full version.

Built by the founder of the **Relationship Clarity Workbook** — the quiz delivers the same
framework value in 15 minutes instead of 6+ hours of reading.

---

## REPO STRUCTURE

```
claritybuddy/
├── CLAUDE.md                  ← you are here
├── .env                       ← secrets, never commit
├── .env.example               ← template, safe to commit
├── .gitignore
├── README.md
├── supabase_schema.sql        ← full DB schema, run once in Supabase SQL editor
│
├── frontend/                  ← deployed to Vercel (free)
│   ├── index.html             ← landing page
│   ├── quiz.html              ← Quiz 1, 20 questions, one at a time
│   ├── compatibility.html     ← Quiz 2, 15 questions
│   ├── report.html            ← free preview + paywall + full reveal
│   ├── thankyou.html          ← post-payment confirmation
│   ├── css/
│   │   └── main.css           ← all styles, mobile-first
│   ├── js/
│   │   ├── api.js             ← all fetch() calls to backend (uses window.CB_API_URL)
│   │   ├── quiz.js            ← progress bar, navigation, answer collection
│   │   └── payment.js         ← Razorpay checkout flow
│   └── vercel.json            ← Vercel config (cleanUrls + Permissions-Policy header)
│
└── backend/                   ← deployed to Railway (~₹500/mo, always-on)
    ├── main.py                ← FastAPI app + all routes
    ├── openai_service.py      ← GPT prompt builder + API call + response parsing
    ├── razorpay_service.py    ← payment order + signature verification
    ├── database.py            ← Supabase client wrapper
    ├── models.py              ← Pydantic request/response models
    ├── prompts/
    │   ├── quiz1_system.txt   ← GPT system prompt for Quiz 1
    │   ├── quiz2_system.txt   ← GPT system prompt for Quiz 2
    │   └── coach_system.txt   ← GPT system prompt for AI Clarity Coach (subscription)
    ├── requirements.txt
    ├── railway.json
    └── .env.example
```

---

## TECH STACK — DECISIONS LOCKED

| Layer | Choice | Reason |
|---|---|---|
| Frontend hosting | Vercel | Free, auto-deploy on git push |
| Backend | Python FastAPI | Clean, fast, easy async |
| Backend hosting | Railway | Always-on, ~₹500/mo, no cold starts |
| Database | Supabase | Free tier, Postgres, simple API |
| AI | OpenAI GPT-4o-mini | ~₹0.80/report, fast |
| Payments | Razorpay | India-first, UPI support |
| Email | Brevo (future) | Free 300/day |

**No WordPress. No plugins. Pure HTML/CSS/JS frontend + Python backend.**

---

## ENVIRONMENT VARIABLES

All secrets go in `.env` at repo root AND in Railway dashboard for production.
Never hardcode. Never commit `.env`.

```bash
# .env
OPENAI_API_KEY=sk-...
RAZORPAY_KEY_ID=rzp_live_...
RAZORPAY_KEY_SECRET=...
RAZORPAY_WEBHOOK_SECRET=...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=...
FRONTEND_URL=https://claritybuddy.vercel.app
```

---

## BACKEND API ROUTES

```
GET  /health                        ← health check, returns {"status":"ok"}

POST /api/submit-quiz1              ← Quiz 1 answers → GPT → save → returns report_id + persona + score
POST /api/submit-quiz2              ← Quiz 2 answers → GPT → save → returns report_id + score

GET  /api/report/{report_id}        ← returns persona + score + paid status (always free)
GET  /api/report/{report_id}/full   ← returns full report (only if paid=true in DB), 402 if not paid

POST /api/create-payment            ← creates Razorpay order, returns order_id + amount + key_id
POST /api/verify-payment            ← verifies Razorpay signature after frontend payment, marks paid=true
POST /api/webhook/razorpay          ← Razorpay server webhook (payment.captured, subscription events)

POST /api/coach/chat                ← AI Clarity Coach chat (requires active subscription)
```

**CORS**: allows `FRONTEND_URL` env var, localhost:5500/3000, and `*.vercel.app` via regex.

---

## DATABASE SCHEMA (Supabase)

Full schema is in `supabase_schema.sql`. Row Level Security is enabled — only the service key (backend) can read/write.

```sql
-- reports table
id               uuid primary key
email            text not null
name             text
quiz_type        text  -- 'quiz1' or 'quiz2'
answers          jsonb -- all answers as key-value
partner_name     text  -- Quiz 2 only

-- GPT output (written after generation)
archetype        text
score            int   -- 0-100
full_report      text  -- raw GPT text
strengths        text
blind_spots      text
journal_prompts  jsonb -- list of strings
next_step        text

-- Quiz 2 extras
dimensions       jsonb -- { emotional, communication, lifestyle, values, growth, future } each /10
green_flags      text
risk_zones       text
decision         text

-- Payment
paid             boolean default false
payment_id       text  -- Razorpay payment ID after success
created_at       timestamptz default now()

-- subscriptions table
id                        uuid primary key
email                     text unique
plan                      text  -- 'monthly' or 'annual'
status                    text  -- 'active' | 'cancelled' | 'expired'
razorpay_subscription_id  text
expires_at                timestamptz
created_at / updated_at   timestamptz
```

---

## PRICING

| Tier | Price | What they get |
|---|---|---|
| Free | ₹0 | Persona name + score number only |
| Single Report | ₹299 | Full AI report — Quiz 1 OR Quiz 2 |
| Combo Report | ₹499 | Both quizzes full reports |
| Monthly | ₹399/mo | Both + retake every 90 days + AI Coach |
| Annual | ₹2,999/yr | Same as monthly, billed annually |

Plan keys used in code: `'single'`, `'combo'`, `'monthly'`, `'annual'`

---

## THE 5 PERSONAS (Quiz 1 output)

1. **The Guarded Protector** — High self-awareness, walls up, fear of vulnerability
2. **The Hopeful Healer** — Over-gives, attracted to unavailable men, fixes not loves
3. **The Clarity Seeker** — Analytical, good values, analysis paralysis
4. **The Pressure Pleaser** — Decides by family/social timeline, not own wants
5. **The Grounded Chooser** — Aspirational goal persona, chooses from clarity

---

## QUIZ 1 — SELF REFLECTION (20 questions)

**Section A: Identity & Values (Q1–Q5)**
Q1: Non-negotiables in a relationship
Q2: Identity outside relationships
Q3: Response when someone violates your values
Q4: Core values in a relationship
Q5: Clarity on non-negotiables

**Section B: Emotional Readiness (Q6–Q10)**
Q6: Reaction when a stable man shows interest
Q7: How much past hurt affects present decisions
Q8: How it feels to be in a relationship right now
Q9: Trust in own judgement evaluating a partner
Q10: Response to family/society pressure about marriage

**Section C: Love Patterns (Q11–Q15)**
Q11: Type of men attracted to in the past
Q12: Emotional experience in past relationships
Q13: What you did when a relationship was clearly wrong
Q14: Role you usually take in relationships
Q15: Which fear feels most familiar

**Section D: Relationship Structure (Q16–Q20)**
Q16: Ideal communication style
Q17: Lifestyle description
Q18: Emotional closeness preference
Q19: What matters most for long-term future
Q20: How the ideal relationship in 5 years feels

Answer keys: `q1`–`q20`, values `'a'|'b'|'c'|'d'`. Full question text is in `frontend/quiz.html`.

---

## QUIZ 2 — COMPATIBILITY CHECK (15 questions)

6 dimensions, 2–3 questions each. Answer keys: `eq1`, `eq2`, `cq1`, `cq2`, `lq1`, `lq2`, `vq1`, `vq2`, `gq1`, `gq2`, `fq1`, `fq2`, `overall`.

1. Emotional Compatibility (`eq1`, `eq2`)
2. Communication Compatibility (`cq1`, `cq2`)
3. Lifestyle Compatibility (`lq1`, `lq2`)
4. Values Compatibility (`vq1`, `vq2`)
5. Growth & Ambition Compatibility (`gq1`, `gq2`)
6. Future Vision Compatibility (`fq1`, `fq2`)

Score: each dimension 1–10, total out of 60.
- 50–60: High Compatibility Zone
- 40–49: Strong Compatibility Zone
- 30–39: Caution Zone
- Below 30: High Risk Zone

---

## GPT REPORT STRUCTURE (Quiz 1)

System prompt lives in `backend/prompts/quiz1_system.txt`.
Report must use EXACTLY these 6 sections:
1. YOUR CLARITY PERSONA
2. YOUR STRENGTHS
3. YOUR BLIND SPOTS
4. YOUR CLARITY SCORE
5. YOUR JOURNAL PROMPTS
6. YOUR NEXT STEP

Tone: warm, honest, non-judgmental. Like a trusted older sister.
Always reference the user's specific answers directly. Never generic.

Clarity score guide:
- 80–100: Deep self-awareness, ready to choose well
- 60–79: Good foundation, specific areas to strengthen
- 40–59: Important patterns to address before dating seriously
- Below 40: Significant healing work needed first

---

## GPT REPORT STRUCTURE (Quiz 2)

System prompt lives in `backend/prompts/quiz2_system.txt`.
Parsed sections: COMPATIBILITY SCORE, DIMENSION SCORES, GREEN FLAGS, RISK ZONES, DECISION, JOURNAL PROMPTS.
`archetype` field in DB is set to `"Compatibility Score: {score}/60"` for Quiz 2 reports.

---

## AI CLARITY COACH

- **Route**: `POST /api/coach/chat`
- **Access**: Active subscription required (checked via `subscriptions` table)
- **System prompt**: `backend/prompts/coach_system.txt` — personalised per user by injecting their persona, score, key answers, and blind spots/strengths from their report
- **Model**: GPT-4o-mini, max 500 tokens, temp 0.8
- **Context window**: last 10 conversation turns sent to OpenAI
- **Payload**: `{ report_id, message, history: [{role, content}] }`

---

## DESIGN SYSTEM

Fonts: Playfair Display (headings) + Jost (body) from Google Fonts
All loaded in `<head>` of every HTML file.

```css
/* Brand tokens — defined in css/main.css */
--cream:      #FAF7F2;   /* page background */
--warm:       #F4EDE3;   /* section alt background */
--terra:      #C0644A;   /* primary brand colour */
--terra-deep: #9E4C35;   /* hover state */
--gold:       #C9A060;   /* accent */
--gold-pale:  #EDD9B0;   /* decorative numbers */
--sage:       #8FA48F;   /* checkmarks, success */
--ink:        #281E1A;   /* dark sections, text */
--ink-mid:    #5A4540;   /* body text */
--ink-soft:   #8C7570;   /* secondary text */
--border:     rgba(40,30,26,0.11);
```

Mobile-first. Base styles for 375px. Breakpoints: 640px (tablet), 1024px (desktop).

---

## USER FLOW

```
index.html  →  quiz.html  →  (submits answers)
                                    ↓
                            POST /api/submit-quiz1
                            Backend: GPT generates report
                            Saves to Supabase
                            Returns { report_id, archetype, score }
                                    ↓
                            Redirect → report.html?id={report_id}
                            Shows: persona name + score (free)
                            Blurred: full report sections
                                    ↓
                            User clicks "Unlock Full Report ₹299"
                                    ↓
                            POST /api/create-payment  →  Razorpay order created
                            Razorpay payment modal opens
                                    ↓
                            Payment success in browser
                            POST /api/verify-payment  →  verifies signature, marks paid=true
                            (Razorpay also hits /api/webhook/razorpay as backup)
                                    ↓
                            GET /api/report/{id}/full  →  full report revealed
                                    ↓
                            thankyou.html
                            Upsell: Quiz 2 / Combo / Monthly / Annual plan
```

---

## TARGET USER

Indian unmarried women, 25–45, English-speaking.
Navigating relationships under family pressure and societal timelines.
Key fears: choosing the wrong person, disappointing family, being "too late".
Pain: don't trust their own judgement. Want fast, personal, actionable answers.

---

## BUILD STATUS

All core files are implemented and deployed.

- [x] `frontend/css/main.css` — design tokens + all component styles
- [x] `frontend/quiz.html` — Quiz 1, all 20 questions, one-at-a-time UX
- [x] `frontend/report.html` — preview + paywall + full reveal
- [x] `frontend/index.html` — landing page
- [x] `frontend/compatibility.html` — Quiz 2
- [x] `frontend/thankyou.html` — post-payment page
- [x] `frontend/js/quiz.js` — quiz navigation + answer collection
- [x] `frontend/js/api.js` — all fetch() calls (60s timeout, AbortController)
- [x] `frontend/js/payment.js` — Razorpay integration
- [x] `backend/main.py` — FastAPI routes
- [x] `backend/openai_service.py` — GPT prompt + call + section parsing
- [x] `backend/razorpay_service.py` — payments + webhook + signature verification
- [x] `backend/database.py` — Supabase client
- [x] `backend/models.py` — Pydantic models
- [x] `backend/prompts/quiz1_system.txt` — GPT system prompt
- [x] `backend/prompts/quiz2_system.txt` — GPT system prompt
- [x] `backend/prompts/coach_system.txt` — AI Coach system prompt
- [x] `supabase_schema.sql` — full schema with RLS

---

## CODING CONVENTIONS

- Frontend: vanilla HTML/CSS/JS. No frameworks. No build step.
- All CSS in `css/main.css`. No inline styles except one-offs.
- All API calls in `js/api.js`. Backend URL via `window.CB_API_URL` (set per environment). No fetch() calls scattered in HTML files.
- Backend: FastAPI with async routes. Type hints everywhere. Pydantic models for all inputs/outputs.
- Never hardcode API keys. Always use `os.getenv()`.
- Every backend route returns JSON. HTTP status codes must be correct.
- CORS: backend allows `FRONTEND_URL` env var + localhost ports + `*.vercel.app` regex.
- OpenAI client is module-level singleton with 50s timeout.

---

## COMMANDS

```bash
# Frontend — just open in browser, no build needed
open frontend/index.html

# Backend — local dev
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Deploy frontend
# Push to GitHub → Vercel auto-deploys from /frontend folder

# Deploy backend
# Push to GitHub → Railway auto-deploys from /backend folder
# Railway start command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

*Last updated: 2026-04-28. Update this file whenever a decision changes or a file is completed.*
