# 🚀 Senior Reviewer & Evaluation Guide

Welcome to **TicketLocal** — a high-concurrency movie and live event ticketing engine (BookMyShow / District clone).

---

## ⚡ 60-Second Quickstart (Zero-Friction)

The application has **built-in automatic fallbacks** (SQLite + FakeRedis in-memory engine). **Docker is optional**; you can run the entire stack locally with standard Python and Node.

### Step 1: Environment Keys Setup
Copy the template configuration keys:
- **Windows**: Run `setup_env.bat` or run:
  ```powershell
  copy .env.example backend\.env
  ```
- **macOS / Linux**: Run `chmod +x setup_env.sh && ./setup_env.sh` or run:
  ```bash
  cp .env.example backend/.env
  ```

---

### Step 2: Start Backend (Port 8000)

```bash
cd backend

# Option A: With pip / venv
python -m venv .venv
# Windows: .venv\Scripts\activate | Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Option B: With uv (faster)
uv pip install -r requirements.txt
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

* Backend health & Swagger API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Automatic DB seeding runs on server startup.

---

### Step 3: Start Frontend (Port 5173)

In a second terminal:
```bash
cd frontend
npm install
npm run dev
```

* Web UI: [http://localhost:5173](http://localhost:5173)

---

## 🐳 Optional: Native Docker Mode (PostgreSQL + Redis)

If you prefer full containerized PostgreSQL and Redis:
```bash
docker-compose up -d
```
The backend automatically connects to Postgres on `:5432` and Redis on `:6379`.

---

## 🔑 Key Environment Variables Reference

Located in `backend/.env` (cloned from `.env.example`):

| Variable | Default Value | Purpose |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://ticketlocal:ticketlocal_secret@localhost:5432/ticketlocal_db` | Postgres connection string (auto-fallbacks to SQLite if unreachable) |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis for distributed seat locks (auto-fallbacks to FakeRedis) |
| `REDIS_LOCK_TTL_SECONDS`| `600` | 10-minute hold countdown for selected seats |
| `SECRET_KEY` | `ticketlocal-super-secret-jwt-key-change-in-production` | JWT signing secret |
| `CONVENIENCE_FEE_PERCENTAGE` | `0.10` | 10% convenience fee calculation |
| `GST_TAX_PERCENTAGE` | `0.18` | 18% GST tax rate calculation |
| `WEEKEND_SURGE_MULTIPLIER` | `1.25` | +25% pricing surge on Friday-Sunday shows |
| `PRIME_TIME_SURGE_MULTIPLIER` | `1.15` | +15% pricing surge between 18:00 - 22:00 |

---

## 🧪 Concurrency & ACID Test Suite

To run the automated concurrency tests:
```bash
cd backend
python -m pytest tests/ -v
```

### What These Tests Verify:
1. `test_concurrency.py`: 50 concurrent simulated users racing for the identical seat. Exactly 1 acquires the lock; 49 receive `423 Locked`.
2. `test_double_booking_prevention.py`: Cache is wiped mid-checkout; PostgreSQL `UNIQUE (show_id, seat_id)` constraint prevents double-booking and returns `409 Conflict`.
3. `test_pricing.py`: Validates Standard, Premium, and Recliner multipliers, weekend surges, and prime-time surges.
4. `test_ttl_expiry.py`: Tests 600s TTL countdown in seat matrix and hold release upon payment failure.

---

## 👤 Pre-Seeded Test Credentials

- **Customer Account**: `demo@ticketlocal.com` / `Demo@1234`
- **Admin Account**: `admin@ticketlocal.com` / `Admin@1234`
- **Simulated Payment Gateway**:
  - *Successful Card*: `4000 1234 5678 9010` (Exp: `12/28`, CVV: `123`)
  - *Decline Simulation*: `4000 0000 0000 0002` (Exp: `11/29`, CVV: `999`)

---

## 🎯 Special Features to Review in UI

1. **SVG Curved Cinema Map**: Dynamic realistic seat curvature, seat tiers (Standard ₹250, Premium ₹380, Recliner ₹550).
2. **Real-Time Hold Countdown**: 10-minute countdown timer with sync to server TTL.
3. **High-Fidelity QR Tickets**: Automatic offline QR code generation embedded into tickets.
4. **Chaos Testing Lab** (`/chaos`): Trigger cache flushes, simulated DB contention, and tax errors in real time.
