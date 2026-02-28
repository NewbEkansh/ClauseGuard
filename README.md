# ClauseGuard – AI Contract Risk Intelligence System

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Next.js](https://img.shields.io/badge/frontend-Next.js-black.svg)

**ClauseGuard** is an AI-powered contract risk analysis platform that extracts, scores, and audits high-risk clauses from legal documents using LLM-driven semantic analysis.

The system combines background task processing (Celery), structured clause storage (PostgreSQL), audit logging, and an analytics-driven admin dashboard to provide real-time contract intelligence.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Redis (local)
- PostgreSQL (Supabase or local)
- Groq API Key

---

## Backend Setup

```bash
git clone <repo-url>
cd ClauseGuard
python -m venv venv
source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
DATABASE_URL=postgresql://...
REDIS_URL=redis://localhost:6379/0
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
DEV_MODE=false
JWT_SECRET=your_jwt_secret
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_admin_password
```

### Start Services

```bash
# Start Redis
redis-server

# Start Backend API
uvicorn backend.main:app --reload --port 8080

# Start Celery Worker
celery -A backend.celery_worker.celery worker --loglevel=info
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:3000`

---

## 🧠 Core Capabilities

### 1. Intelligent Clause Extraction
- Extracts full contract text from PDFs
- Identifies relevant risk-bearing sections
- Sends contextual text to LLM for semantic analysis

### 2. Risk Scoring Engine
- Returns structured JSON analysis
- Calculates overall contract risk score (0–100)
- Persists structured clause data in database

### 3. Background Processing (Celery)
- Asynchronous contract analysis
- Retry logic on LLM failures
- Fault-tolerant, scalable worker architecture

### 4. Audit Logging
- Upload events, analysis start/completion
- Failure tracking and retry attempts
- Admin activity logs

### 5. Admin Analytics Dashboard
- Real-time system metrics
- Filtering, pagination, and JWT-protected access

---

## 🏗 System Architecture

```
Frontend (Next.js)
        ↓
FastAPI Backend
        ↓
Celery Worker (Async AI Processing)
        ↓
LLM Engine (Groq)
        ↓
PostgreSQL (Supabase)
        ↓
Redis (Task Broker)
```

---

## 📁 Project Structure

```
ClauseGuard/
│
├── backend/
│   ├── api/
│   │   ├── upload.py
│   │   ├── admin.py
│   │   ├── auth.py
│   │   └── analysis.py
│   │
│   ├── models/
│   │   ├── contract.py
│   │   ├── clause.py
│   │   ├── audit_log.py
│   │   └── db.py
│   │
│   ├── services/
│   │   ├── llm_engine.py
│   │   ├── pdf_parser.py
│   │   ├── clause_retriever.py
│   │   ├── audit_service.py
│   │   └── auth_service.py
│   │
│   ├── tasks/
│   │   └── analyze_contract.py
│   │
│   ├── celery_worker.py
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── app/
│   ├── components/
│   └── styles/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🔬 Technical Workflow

**1. Contract Upload**
- PDF uploaded via API
- Contract record created in DB
- Celery task triggered asynchronously

**2. Async AI Analysis**
```python
# Extract full PDF text
# Retrieve relevant sections
# Send to LLM for semantic analysis
# Compute risk score
# Persist clause data and update contract record
```

**3. Risk Scoring**
- AI returns structured JSON
- Overall risk score (0–100) computed
- Clause data stored in PostgreSQL

**4. Admin Review**
- View contract status and clause breakdown
- Review audit logs and risk distribution

---

## 📊 Admin Dashboard

- Contract lifecycle tracking (`processing` / `completed` / `failed`)
- Risk filtering (min/max range)
- Status filtering
- Animated stat counters
- JWT-protected access

---

## 🔐 Security

- JWT-based authentication
- Hashed admin credentials (bcrypt)
- Role-protected admin routes
- Structured audit logging
- No direct database exposure to frontend

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| Task Queue | Celery + Redis |
| Database | PostgreSQL (Supabase) + SQLAlchemy |
| Auth | python-jose (JWT) |
| LLM | Groq API |
| Frontend | Next.js, TailwindCSS |
| Animations | Framer Motion |

---

## 🎯 Use Cases

1. Enterprise contract risk screening
2. Legal due diligence automation
3. Compliance monitoring
4. Vendor agreement evaluation
5. SaaS contract intelligence platforms

---

## 🧠 Future Enhancements

- Multi-user support with role-based access control
- AI clause explanation visualization
- Vector embeddings for clause similarity search
- Model fine-tuning on legal corpora
- S3 storage integration
- Contract versioning history

---

## ⚠️ Limitations

- AI results depend on model quality and are not a substitute for legal advice
- Requires well-formatted PDF input
- Risk scoring is heuristic-based

---

## 📜 License

MIT License

---

*ClauseGuard – Intelligent Contract Risk Intelligence | v1.0 | Async AI Microservice Architecture*