# TicketLocal 🎟️

TicketLocal is a high-concurrency, production-style movie and live event ticketing platform (BookMyShow / District clone). It is designed to handle high ticket demand with distributed seat locks, ACID transactions, dynamic pricing rules, interactive SVG seat maps, and offline QR ticket generation.

---

## 🌟 Key Features

1. **Atomic Distributed Seat Locking (Redis 600s TTL)**:
   - Atomic multi-key acquisition with rollback on contention.
   - HTTP `423 Locked` returned with conflicting seat IDs.
   - Idempotent holds for the same user with real-time countdown.
2. **PostgreSQL ACID Guarantee**:
   - `UNIQUE (show_id, seat_id)` constraint on `booking_seats` as the ultimate defense against double-booking.
3. **Dynamic Surge & Seat-Tier Pricing**:
   - Standard, Premium, and Recliner multipliers.
   - Weekend surge (+25%) and Prime-Time evening surge (18:00–22:00, +15%).
   - Itemized 10% convenience fee + 18% GST tax calculation.
4. **Interactive SVG Curved Seat Map**:
   - Visual cinema curvature with realistic screen glow.
   - Available, Selected, Held (amber pulsing lock), and Booked seat states.
   - Polling every ~5 seconds for live multi-user updates.
5. **Offline QR Ticket Generation**:
   - High-fidelity QR code PNG tickets generated in the background via threadpool (`run_in_threadpool`).
6. **Resilience Chaos Lab (`/chaos`)**:
   - Real-time in-process metrics (`/api/metrics-lite`): active locks, 423 contentions, checkout abandonment rate.
   - Fault injections: Cache lock drop (simulates double-booking risk), DB table lock contention, tax calculation crash (`ZeroDivisionError`), synchronous QR storm.

---

## 🏗️ Architecture & Tech Stack

- **Backend**: Python 3.11+, FastAPI (async), SQLAlchemy 2.0 (async), Pydantic v2
- **Database**: PostgreSQL (local / Docker) + SQLite aiosqlite automatic fallback
- **Distributed Cache & Locks**: Redis (`redis.asyncio`) + in-memory `fakeredis` fallback
- **QR Engine**: `qrcode` + `Pillow` (threadpool execution)
- **Authentication**: JWT Bearer token + bcrypt password hashing
- **Frontend**: Vue 3 (Composition API, `<script setup>`), Vite, Pinia, Vue Router, Tailwind CSS, Canvas Confetti

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.11+ (or `uv`)
- Node.js 18+ and npm
- Docker (optional, for native PostgreSQL and Redis)

### 2. Start PostgreSQL & Redis (Optional Docker Compose)
```bash
docker-compose up -d
```

### 3. Backend Setup
```bash
cd backend

# Create virtual environment & install dependencies (or with uv)
uv pip install -r requirements.txt

# Run migrations & seed data
uv run python app/seed.py

# Start FastAPI development server
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
*API Swagger Documentation will be available at:* `http://127.0.0.1:8000/docs`

### 4. Frontend Setup
```bash
cd frontend

# Install packages
npm install

# Start Vite development server
npm run dev
```
*Frontend Web Application will be available at:* `http://localhost:5173`

---

## 🧪 Running the Pytest Test Suite

The test suite covers full concurrency stress testing, ACID double-booking prevention, pricing surges, and TTL expiry:
```bash
cd backend
$env:PYTHONPATH="."
uv run python -m pytest tests/ -v
```

### Test Coverage Highlights:
- `test_concurrency.py`: 50 simultaneous users compete for the same seat — exactly 1 succeeds, 49 get `423 Locked`.
- `test_double_booking_prevention.py`: Cache is wiped mid-checkout — PostgreSQL `UNIQUE(show_id, seat_id)` constraint catches double booking with `409 Conflict`.
- `test_pricing.py`: Verifies Standard, Premium, Recliner multipliers, weekend surges, and prime-time surges.
- `test_ttl_expiry.py`: Tests 600s TTL countdown in seat matrix and hold retention upon mock payment failure.

---

## 📋 Default Credentials

- **Demo Citizen User**: `demo@ticketlocal.com` / `Demo@1234`
- **Admin User**: `admin@ticketlocal.com` / `Admin@1234`
- **Mock Payment Cards**:
  - *Valid Card (Success)*: `4000 1234 5678 9010`, Exp: `12/28`, CVV: `123`
  - *Decline Card (Simulation)*: `4000 0000 0000 0002`, Exp: `11/29`, CVV: `999`
