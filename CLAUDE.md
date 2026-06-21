# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Context

This repo supports the **Programa AI-First · Fase 1** — a 4-week preparation course followed by the Reto Fase 1. Full program details in `programa-ai-first-fase1.md` (+ `.pdf`).

### Program structure

| Week | Theme |
|------|-------|
| 1 | Claude CLI + Spec Engineering (2 workshops) |
| 2 | CLAUDE.md (2 workshops) |
| 3 | Plan & Loop · MCP Servers · Subagents · Git (2 workshops) |
| 4 | **Reto Fase 1** — DEV track + QA track in parallel |

**Foundational rule:** every AI project starts with `/init`. This generates the base `CLAUDE.md` and establishes the AI contract before any spec or code.

### Two tracks in Week 4

**Track DEV** — build an end-to-end product (backend + frontend + DB + integration) in 4 days, free idea, no manual code, via Hermes.

**Track QA** — design and execute a full test strategy on `mini-tienda-base` (the SUT in this repo) in 4 days, no manual scripts, via Hermes. Goal is NOT to modify the app — test it.

Both tracks deliver: repo + `HERMES_CONTEXT.md` + 5–7 min demo on Friday.

## Running the SUT (System Under Test)

```bash
# Docker (recommended)
cd mini-tienda-base
docker compose up --build

# Python local
cd mini-tienda-base
pip install -r requirements.txt
uvicorn app:app --port 8000

# Simulate pricing service failure
PRICING_FAIL=1 uvicorn app:app --port 8000

# Use a separate DB for tests (avoid polluting dev data)
DB_PATH=test.db uvicorn app:app --port 8001
```

App runs at `http://localhost:8000`. Interactive API docs at `http://localhost:8000/docs`.

## API Contract

All monetary amounts are in **centavos** (integer cents).

| Method | Route | Notes |
|--------|-------|-------|
| GET | `/api/health` | Returns `{"status": "ok"}` |
| GET | `/api/products` | List all products |
| GET | `/api/products/{id}` | 404 if not found |
| GET | `/api/pricing/quote?subtotal_cents=N&country=XX` | 503 if `PRICING_FAIL=1` |
| POST | `/api/orders` | Body: `{country, items: [{product_id, qty}]}`. 201 on success, 400/409/503 on error |
| GET | `/api/orders/{id}` | Includes nested `items` array |

Tax rates: `CO` → 19%, `US` → 0%, any other → 10%. Tax computed as `int(subtotal * rate)` (truncates, does not round).

## Architecture of the SUT

```
mini-tienda-base/
  app.py          # Single-file FastAPI backend — all routes, DB, and business logic
  static/
    index.html    # Single-page frontend (vanilla JS, no build step)
  requirements.txt
  Dockerfile
  docker-compose.yml
```

SQLite DB (`minitienda.db`) is created and seeded on first startup. The `DB_PATH` env var controls the DB file location — use a separate file for test isolation.

The "pricing service" is an internal function (`price_quote`) — not an external HTTP call. It is toggled via `PRICING_FAIL=1`.

## Known Defects (Ground Truth — Internal)

These are intentional weaknesses planted in the SUT for evaluation depth:

1. **No qty validation** — `qty=0` or `qty=-1` is accepted; negative qty inflates stock and produces negative totals.
2. **Tax truncation** — uses `int()` instead of `round()`; e.g., 10% of 1005 → 100 instead of 101.
3. **Country case-sensitive** — `country="co"` (lowercase) falls through to 10% default instead of 19%.

Good test coverage should catch at minimum defects 1 and 3. The `PRICING_FAIL=1` 503 scenario is also expected.

## Test Strategy Scope

Tests must cover all these dimensions:

- **API contract** — HTTP status codes, required response fields, error shapes
- **Functional** — happy path, edge cases, negative cases for every endpoint
- **Data integrity** — stock is decremented correctly after order; order totals match arithmetic
- **Integration failure** — `PRICING_FAIL=1` yields 503 on both `/api/pricing/quote` and `POST /api/orders`
- **UI / E2E** — purchase flow via the frontend

Recommended tools: **Playwright** for E2E/UI, **pytest + httpx** for API.

## Required Deliverable Files

| File | Purpose |
|------|---------|
| `HERMES_CONTEXT.md` | Process log: scope, tooling, AI usage, decisions, findings, blockers |
| Test plan doc | Strategy, scope, risks, acceptance criteria |
| Test cases | Happy path + edge + negative, documented |
| Automated E2E suite | Playwright or equivalent, runnable against localhost:8000 |
| API test suite | Contract + error validation |
| Defect report | Findings with severity, repro steps, evidence |
