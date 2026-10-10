# Week 2: Software Development Concepts & FastAPI Microservice

---
relevancy_tier: CAUTIONARY_ANTI_PATTERN
mentor_score: 75/100
classroom_id: 854212456010
quiz_id: 863309954466
local_path: F:\FuseAIF2026\M1\WK2
github_repo: https://github.com/AaradhyaDT/fuseAiF_wk2_customer_api_app
---

## 1. Overview & Theoretical Objectives
- **Scenario**: Backend / Systems Engineer building database infrastructure for customer analytics.
- **Tasks**:
  1. **PostgreSQL Setup**: Containerized database initialization via Docker Compose seeded with `seed.sql`.
  2. **FastAPI Endpoint (`customers` table)**: Develop REST API with SQLAlchemy ORM and Pydantic schemas.
  3. **Concurrency & Modularity**: Aggregate record counts across all relational tables concurrently using `asyncio.gather`.

---

## 2. The Mentor Anti-Pattern Penalty & Architectural Invariant (`INV-FUSE-ROUTER`)

> [!WARNING]
> **Instructor Critique (Penalized: 75 / 100)**:
> In the original submission, API routes, database session management, ORM models, and business logic were grouped inside a single monolithic `main.py`. The fellowship mentor flagged this structure:
> *"Declutter into subfolders; separate `APIRouter` per domain instead of monolithic single-file API."*

### Mandatory Corrective Pattern for All New Projects:
Never deploy a single-file FastAPI server. Enforce strict 4-layer separation:
```
app/
├── core/
│   ├── config.py         # BaseSettings reading from .env
│   └── database.py       # create_async_engine & async_sessionmaker
├── models/
│   └── customer.py       # SQLAlchemy Base Declarative Table
├── schemas/
│   └── customer.py       # Pydantic v2 CustomerCreate, CustomerResponse
├── routers/
│   ├── health.py         # Liveness/readiness probes
│   └── customers.py      # APIRouter(prefix="/customers", tags=["Customers"])
└── main.py               # Minimal FastAPI() app mounting routers
```

---

## 3. SOTA Industry Best Practices & Production Standards
- **SQLAlchemy 2.0 Async Pipeline**: Use `create_async_engine("postgresql+asyncpg://...")` with scoped sessions.
- **Pydantic v2 `model_validate`**: Enable `model_config = ConfigDict(from_attributes=True)` for seamless ORM-to-schema serialization.
- **Concurrent Table Aggregations**:
  ```python
  import asyncio
  from sqlalchemy import func, select
  from app.core.database import async_session
  from app.models import Customer, Order, Product

  async def get_table_count(model) -> dict:
      async with async_session() as session:
          stmt = select(func.count()).select_from(model)
          result = await session.execute(stmt)
          return {model.__tablename__: result.scalar_one()}

  async def aggregate_all_counts():
      models = [Customer, Order, Product]
      # Run all count queries concurrently across connection pool
      results = await asyncio.gather(*(get_table_count(m) for m in models))
      return {k: v for d in results for k, v in d.items()}
  ```

---

## 4. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directory**: [`F:\FuseAIF2026\M1\WK2`](file:///F:/FuseAIF2026/M1/WK2)
  - `main.py` — Original implementation script.
  - `app/` — Application source folder.
  - `docker-compose.yml` — Container configuration for PostgreSQL.
  - `Dockerfile` — Python application container specification.
  - `requirements.txt` / `pyproject.toml` — Dependency pins.
- **GitHub Remote Fallback**:
  - `https://github.com/AaradhyaDT/fuseAiF_wk2_customer_api_app`
  - Clone: `gh repo clone AaradhyaDT/fuseAiF_wk2_customer_api_app`

---

## 5. Classroom Quiz Analysis & Conceptual Traps
- **Quiz ID**: `863309954466` ("Agentic Software Development Quiz", Handed in).
- **Event Loop Starvation Trap**: Placing `time.sleep()` or synchronous database calls (`psycopg2.connect`) inside an `async def` route blocks the entire single-threaded Python event loop, collapsing API throughput to 1 request at a time.
- **Docker Volume Persistence**: If Docker Compose does not define a named volume for PostgreSQL data (`/var/lib/postgresql/data`), destroying the container (`docker compose down`) permanently destroys all seeded tables.
