-- ClarityBuddy — Supabase Schema
-- Run this once in Supabase → SQL Editor → New Query

-- ── Reports table ─────────────────────────────────────────
create table if not exists reports (
  id               uuid primary key default gen_random_uuid(),
  email            text not null,
  name             text,
  quiz_type        text not null check (quiz_type in ('quiz1', 'quiz2')),
  answers          jsonb not null default '{}',
  partner_name     text,

  -- GPT output
  archetype        text,
  score            int check (score >= 0 and score <= 100),
  full_report      text,
  strengths        text,
  blind_spots      text,
  journal_prompts  jsonb default '[]',
  next_step        text,

  -- Quiz 2 extras
  dimensions       jsonb,
  green_flags      text,
  risk_zones       text,
  decision         text,

  -- Payment
  paid             boolean not null default false,
  payment_id       text,

  created_at       timestamptz not null default now()
);

-- Index for quick lookups by email
create index if not exists reports_email_idx on reports(email);

-- ── Subscriptions table ───────────────────────────────────
create table if not exists subscriptions (
  id                        uuid primary key default gen_random_uuid(),
  email                     text not null unique,
  plan                      text not null check (plan in ('monthly', 'annual')),
  status                    text not null default 'active' check (status in ('active', 'cancelled', 'expired')),
  razorpay_subscription_id  text,
  expires_at                timestamptz,
  created_at                timestamptz not null default now(),
  updated_at                timestamptz not null default now()
);

create index if not exists subscriptions_email_idx on subscriptions(email);

-- ── Row Level Security (optional but recommended) ─────────
-- Disable public read/write — only service key (backend) can access
alter table reports       enable row level security;
alter table subscriptions enable row level security;

-- No public policies = only service_role key can read/write
-- Your FastAPI backend uses the service key, so this is correct.
