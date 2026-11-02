# AI-Powered Customer Support Automation Platform

A production-ready, enterprise-grade AI customer support platform that autonomously classifies incoming customer tickets, extracts semantic embeddings, queries a vector knowledge base, synthesizes context-grounded responses without hallucination, and escalates complex or critical cases to human support agents with least-loaded routing.

---

## Architecture Overview

```
                          ┌──────────────────────────┐
                          │   React 18 + TS Client   │
                          │   (Tailwind + Recharts)  │
                          └─────────────┬────────────┘
                                        │ HTTP / REST / JWT
                                        ▼
                          ┌──────────────────────────┐
                          │     FastAPI Gateway      │
                          │   (Pydantic + RBAC Auth) │
                          └──────┬────────────┬──────┘
                                 │            │
            ┌────────────────────┘            └────────────────────┐
            ▼                                                      ▼
  ┌───────────────────┐                                  ┌───────────────────┐
  │   PostgreSQL 16   │                                  │   Redis Broker    │
  │    + pgvector     │                                  │   (Celery Task    │
  │ (10 Norm. Tables) │                                  │      Queue)       │
  └───────────────────┘                                  └─────────┬─────────┘
                                                                   │
                                                                   ▼
                                                         ┌───────────────────┐
                                                         │   Celery Worker   │
                                                         │ (Async Pipeline)  │
                                                         └─────────┬─────────┘
                                                                   │
                         ┌─────────────────────────────────────────┴─────────┐
                         ▼                                                   ▼
            ┌─────────────────────────┐                         ┌─────────────────────────┐
            │   Classification Engine │                         │   Semantic Retrieval    │
            │  (OpenAI + Deterministic│                         │   (1536d Cosine Search  │
            │        Fallback)        │                         │   pgvector / NumPy)     │
            └────────────┬────────────┘                         └────────────┬────────────┘
                         │                                                   │
                         └────────────────────┬──────────────────────────────┘
                                              ▼
                                 ┌─────────────────────────┐
                                 │   Grounded Response     │
                                 │      Generation &       │
                                 │ Least-Loaded Routing    │
                                 └─────────────────────────┘
```

---

## Key Highlights & Empirical Performance

The platform was subjected to a formal, reproducible benchmark evaluating **250 realistic customer support scenarios** spanning 7 diverse ticket categories.

| Metric | Target | Measured Result | Status |
| :--- | :---: | :---: | :---: |
| **Classification Accuracy** | $\ge 86.0\%$ | **98.8%** (247 / 250) | **PASSED** |
| **Routing / Escalation Accuracy** | $\ge 86.0\%$ | **88.0%** (220 / 250) | **PASSED** |
| **Latency Reduction vs Baseline** | $\ge 24.0\%$ | **80.75%** (1.28 ms vs 6.65 ms) | **PASSED** |
| **Confidence Calibration Score** | - | **0.933 / 1.000** | **OPTIMAL** |
| **Automated Test Suite** | 100% pass | **26 / 26 passing** | **PASSED** |

---

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+) with asynchronous lifecycle management
- **Data Validation & Settings**: Pydantic v2 & Pydantic-Settings
- **ORM & Migrations**: SQLAlchemy 2.0 with Alembic database migrations
- **Vector Search**: PostgreSQL `pgvector` (1536-dimensional embeddings) with NumPy zero-dependency cosine fallback
- **Task Queue & Broker**: Celery 5.3 + Redis 7 (supporting eager in-memory testing)
- **Security**: JWT tokens (PyJWT HS256), direct `bcrypt` password hashing, Role-Based Access Control (Admin, Agent, Customer)
- **AI Services**: OpenAI API (`gpt-4o-mini`, `text-embedding-3-small`) with structured Pydantic schema validation, prompt-injection shielding, exponential backoff retries, and comprehensive fallback classifiers.

### Frontend
- **Framework**: React 18, TypeScript, Vite
- **Styling**: Tailwind CSS with custom enterprise design system, CSS variables, and light/dark theme switching
- **Visualizations**: Recharts (Volume area charts, priority distribution donuts, category breakdown bars, benchmark comparison radars)
- **Icons**: Lucide React
- **HTTP Client**: Axios with automatic JWT interceptors and error handling

### Infrastructure & DevOps
- **Containerization**: Multi-stage Docker builds for backend and frontend
- **Reverse Proxy**: Nginx (Alpine) with SPA routing and API reverse-proxy
- **Orchestration**: Docker Compose with health checks, persistent volumes, and development overlays

---

## Database Architecture (10 Normalized Tables)

1. `users`: Stores user identity, hashed passwords, roles (`admin`, `agent`, `customer`), and active status.
2. `tickets`: Stores core ticket details, category, priority, status, customer relation, assigned agent, and `requires_human` flag.
3. `ticket_messages`: Full threaded conversation history between customers, AI, and human support agents.
4. `ticket_classifications`: AI triage metadata: detected category, priority, sentiment, intent, confidence score, and reasoning summary.
5. `knowledge_articles`: Ground truth documentation, FAQs, categories, tags, and publication state.
6. `knowledge_embeddings`: 1536-dimensional vector embeddings for each article for cosine similarity search.
7. `generated_responses`: Draft AI responses grounded strictly in retrieved articles, with confidence metrics and human approval tracking.
8. `agent_assignments`: Assignment audit records linking tickets to agents with assignment status and operational notes.
9. `ticket_escalations`: Escalation events recording reasons, priority changes, escalation initiator, and resolution notes.
10. `processing_tasks`: Asynchronous task lifecycle audit tracking Celery task IDs, retry counts, statuses (`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`), and execution latencies.

---

## Directory Structure

```
ai-support-platform/
├── backend/
│   ├── alembic/                      # Database migration scripts & env.py
│   ├── app/
│   │   ├── api/v1/endpoints/         # Modular REST endpoints (auth, tickets, ai, knowledge, etc.)
│   │   ├── core/                     # Configuration, security, logging, exceptions
│   │   ├── database/                 # SQLAlchemy session engine & pgvector type handler
│   │   ├── models/                   # 10 Normalized SQLAlchemy models
│   │   ├── repositories/             # Repository pattern data access layer
│   │   ├── schemas/                  # Pydantic request/response schemas
│   │   ├── services/                 # AI, classification, embedding, retrieval, routing services
│   │   ├── utils/                    # Seeders, benchmark runners, evaluation dataset generators
│   │   ├── workers/                  # Celery application & asynchronous background tasks
│   │   └── main.py                   # FastAPI entrypoint, lifespan, CORS, and routers
│   ├── data/
│   │   └── evaluation_scenarios_250.json # 250 Predefined evaluation ticket scenarios
│   ├── tests/                        # 26 Pytest unit, integration, and benchmark tests
│   ├── Dockerfile                    # Python 3.11-slim containerfile
│   ├── requirements.txt              # Production Python dependencies
│   └── alembic.ini                   # Alembic migration configuration
├── frontend/
│   ├── src/
│   │   ├── components/               # Navbar, Sidebar, LoginModal, UI elements
│   │   ├── pages/                    # Overview, Tickets, AIInsights, KnowledgeBase, Workspace, Analytics, Simulator
│   │   ├── services/                 # Axios API client & mock failover
│   │   ├── types/                    # Full TypeScript domain contracts
│   │   ├── App.tsx                   # Main SPA state, theme switching, tab navigation
│   │   └── index.css                 # Tailwind typography and theme styles
│   ├── Dockerfile                    # Multi-stage Node builder + Nginx production server
│   ├── nginx.conf                    # Nginx reverse proxy configuration
│   └── package.json                  # Frontend dependencies
├── docker-compose.yml                # Production multi-service Docker configuration
├── docker-compose.dev.yml            # Hot-reloading development overlay
├── run_evaluation.py                 # Standalone 250-scenario reproducible benchmark runner
├── .env.example                      # Documented environment variables template
└── README.md                         # Project documentation
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+ & npm
- Docker & Docker Compose (Optional, for containerized run)

---

### Option A: Local Development Setup

#### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run initial migrations
alembic upgrade head

# Launch FastAPI development server (auto-seeds default users & knowledge base)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
The backend API is now accessible at `http://localhost:8000`. Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

#### 2. Frontend Setup
```bash
cd frontend

# Install npm dependencies
npm install

# Start Vite dev server
npm run dev
```
The React dashboard is now accessible at `http://localhost:5173`.

---

### Option B: Full Docker Compose Deployment

To build and run all 5 containers (PostgreSQL with pgvector, Redis, FastAPI, Celery worker, and React frontend):

```bash
# Copy example configuration
cp .env.example .env

# Build and start services
docker compose up --build -d
```

- **Frontend Dashboard**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **Swagger Documentation**: `http://localhost:8000/docs`
- **Database**: `localhost:5432` (`postgres` / `postgres`)
- **Redis Broker**: `localhost:6379`

---

## Seed Accounts & Role-Based Access Control

The platform initializes with 3 default accounts:

| Role | Email | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@supportplatform.ai` | `AdminPass123!` | Full system access, article publication, ticket deletion, agent reassignment |
| **Support Agent** | `agent.sarah@supportplatform.ai` | `AgentPass123!` | Ticket view, approve AI responses, claim escalations, manage conversation |
| **Customer** | `customer.john@example.com` | `CustomerPass123!` | Submit tickets, view own tickets, reply to customer threads |

---

## REST API Reference

### Authentication
- `POST /api/v1/auth/register` — Register a new customer user account.
- `POST /api/v1/auth/login` — Authenticate with email/password to retrieve JWT access and refresh tokens.
- `POST /api/v1/auth/refresh` — Issue a refreshed JWT access token using a valid refresh token.
- `GET /api/v1/auth/me` — Retrieve the current authenticated user's profile.

### Ticket Management
- `POST /api/v1/tickets` — Submit a support ticket. Triggers asynchronous Celery classification, vector search, response draft, and routing.
- `GET /api/v1/tickets` — List support tickets with pagination, status, category, priority, and search filtering.
- `GET /api/v1/tickets/{ticket_id}` — Get ticket details, classification metadata, and suggested responses.
- `PATCH /api/v1/tickets/{ticket_id}` — Update ticket status, priority, or assigned agent.
- `DELETE /api/v1/tickets/{ticket_id}` — Remove a ticket (Admin role required).

### AI Processing
- `POST /api/v1/ai/classify` — Direct triage analysis on subject/message (returns category, priority, sentiment, intent, confidence).
- `POST /api/v1/ai/generate-response` — Generate a grounded draft response based on ticket context and retrieved articles.
- `GET /api/v1/tickets/{ticket_id}/processing-status` — Poll the asynchronous Celery processing pipeline status.

### Knowledge Base & Vector Search
- `GET /api/v1/knowledge` — List all published knowledge base articles.
- `POST /api/v1/knowledge` — Create and automatically vectorize a new knowledge article.
- `GET /api/v1/knowledge/{article_id}` — Retrieve an article by ID.
- `DELETE /api/v1/knowledge/{article_id}` — Delete a knowledge article and its corresponding embeddings.
- `POST /api/v1/knowledge/search` — Perform cosine similarity vector search over the knowledge base.

### Conversations & Agent Routing
- `GET /api/v1/tickets/{ticket_id}/messages` — Fetch chronological conversation thread.
- `POST /api/v1/tickets/{ticket_id}/messages` — Append customer or agent message to the ticket.
- `GET /api/v1/agents` — List support agents with active ticket load metrics.
- `POST /api/v1/tickets/{ticket_id}/assign` — Assign or reassign ticket to an agent.
- `POST /api/v1/tickets/{ticket_id}/escalate` — Trigger manual or automated escalation with reason and priority adjustment.

### Analytics & Reporting
- `GET /api/v1/analytics/dashboard` — Real-time operational metrics, resolution rates, category breakdowns, and confidence stats.
- `GET /api/v1/analytics/evaluation-benchmark` — Empirical evaluation results from the 250-scenario benchmark.

---

## Running the Automated Test Suite & Benchmark

### 1. Pytest Automated Test Suite
Run the full automated test suite containing 26 comprehensive unit and integration tests:
```bash
cd backend
.\venv\Scripts\pytest.exe -v
```
Output:
```
======================= 26 passed in 9.09s =======================
```

### 2. 250-Scenario Reproducible Benchmark
Execute the formal benchmark directly from the project root:
```bash
python run_evaluation.py
```
Output:
```
======================================================================
      AI-POWERED CUSTOMER SUPPORT PLATFORM: EVALUATION BENCHMARK       
======================================================================
Evaluating 250 Predefined Ticket Scenarios across 7 categories...
--- Running Benchmark on 250 Support Scenarios ---

------------------------- BENCHMARK RESULTS -------------------------
Total Scenarios Evaluated       : 250
Classification Accuracy         : 98.8%  (Target: >= 86.0%)
Routing Accuracy                : 88.0%  (Target: >= 86.0%)
Priority Detection Accuracy     : 73.6%
Retrieval Relevance             : 44.8%
Confidence Calibration Score    : 0.933 / 1.000
------------------------- LATENCY BENCHMARK -------------------------
Average Asynchronous Latency    : 1.28 ms
Synchronous Baseline Latency    : 6.65 ms
Latency Reduction vs Baseline   : 80.75%  (Target: >= 24.0%)
------------------------- TARGET VERIFICATION -----------------------
Target 1 (>=86% Accuracy)       : PASSED
Target 2 (>=24% Latency Drop)   : PASSED
======================================================================
```

---

## Security & Reliability Design Patterns

1. **Prompt Injection Shielding**: Customer messages are parsed as strict user data payloads enclosed in delimited quotation blocks within system instructions. System prompt overrides are rejected, and safety filters detect malicious prompt jailbreak attempts.
2. **Direct Bcrypt Authentication**: Uses robust bcrypt password hashing avoiding known compatibility quirks with 72-byte string boundaries.
3. **Dual Vector Architecture**: Transparently runs against PostgreSQL `pgvector` for native IVFFlat indexing in production while maintaining a zero-dependency NumPy fallback for local testing and CI/CD pipelines.
4. **Idempotent Celery Workers**: Background processing tasks track execution state inside the `processing_tasks` table, preventing duplicate executions when retried under transient network failures.
5. **Grounded Response Generation**: The response generation engine requires explicit context citations and is strictly instructed to avoid inventing external policies or unsupported refunds.
