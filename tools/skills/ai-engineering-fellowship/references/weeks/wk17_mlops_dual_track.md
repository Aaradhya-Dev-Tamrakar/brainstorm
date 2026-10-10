# Week 17: Production MLOps (Dual Track: Churn + Agentic AI)

---
relevancy_tier: GOLDEN_REFERENCE
mentor_score: Turned In
classroom_id: 884301996556
quiz_id: 884296695175
local_path: F:\FuseAIF2026\M5\WK17
github_repo: https://github.com/AaradhyaDT/fuseAiF_wk17_telco_churn_mlops / https://github.com/AaradhyaDT/fuseAiF_wk17_agentic_mlops
---

## 1. Overview & Dual-Track Industrial Architecture
- **Objective**: Productionize end-to-end Machine Learning and Agentic AI operations with automated tracking, data drift monitoring, inference serving, and DAG workflow orchestration.
- **Track A (Telco Customer Churn MLOps Pipeline)**:
  - Dependency Management: `uv` for ultra-fast, deterministic virtual environments.
  - Experiment & Model Registry: **MLflow** tracking training runs, hyperparameters, and model version transitions (`Staging` $\to$ `Production`).
  - Drift & Quality Monitoring: **Evidently AI** monitoring feature distribution shift (K-S tests, Wasserstein distance).
  - Serving & Orchestration: **FastAPI** REST microservice + **Apache Airflow** scheduled DAGs.
- **Track B (Agentic AI MLOps Pipeline)**:
  - Agent Tracking: MLflow Tracing capturing call graphs, token usage, latency, and tool choices.
  - Prompt Governance: Prompt versioning (`prompts/v1`, `v2`, `v3`) with semantic change tracking.
  - Evaluation: Evidently LLM-as-a-judge automated quality checks.
  - Orchestration: Airflow pipeline triggering periodic agent evaluations.

---

## 2. SOTA Industry Best Practices & Production Standards
- **Virtual Environment Speed & Reproducibility**: Replace slow legacy `pip` environments with **`uv`**. Lock environments using `uv.lock` for sub-second container builds.
- **Model Registry Lifecycle**: Never deploy models directly from training scripts. All deployments must pull verified models from the MLflow Model Registry (`models:/TelcoChurnClassifier@champion`).
- **Automated Data Drift Detection**: Use Evidently AI to run Kolmogorov-Smirnov (K-S) tests on continuous variables and Population Stability Index (PSI) on categorical features between inference payloads and baseline distributions.
- **Airflow DAG Idempotency**: Design Airflow DAG tasks to be strictly idempotent (`execution_date` parameterized), allowing safe automated retries on failure.

---

## 3. Mentor Evaluation & Quality Rating
- **Assignment Status**: **Turned In** ("W17: MLOps Assignment").
- **Quiz Status**: Handed in ("W17: MLOps quiz").
- **Quality Standards**: Two complete standalone production repositories with full Docker Compose setups, Airflow DAGs, and MLflow logging.

---

## 4. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directory**: [`F:\FuseAIF2026\M5\WK17`](file:///F:/FuseAIF2026/M5/WK17)
  - `fuseAiF_wk17_telco_churn_mlops/` — Complete Track A codebase.
  - `fuseAiF_wk17_agentic_mlops/` — Complete Track B codebase.
- **GitHub Remote Fallback**:
  - Track A: `https://github.com/AaradhyaDT/fuseAiF_wk17_telco_churn_mlops`
  - Track B: `https://github.com/AaradhyaDT/fuseAiF_wk17_agentic_mlops`
  - Clone A: `gh repo clone AaradhyaDT/fuseAiF_wk17_telco_churn_mlops`
  - Clone B: `gh repo clone AaradhyaDT/fuseAiF_wk17_agentic_mlops`

---

## 5. Golden Implementation Snippets

### Airflow DAG for Automated Drift Evaluation (Track A)
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "aaradhya",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def evaluate_data_drift():
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset
    import pandas as pd
    
    ref_data = pd.read_parquet("/app/data/reference.parquet")
    prod_data = pd.read_parquet("/app/data/current_batch.parquet")
    
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref_data, current_data=prod_data)
    report.save_html("/app/reports/drift_report.html")

with DAG(
    "mlops_drift_monitoring",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:
    drift_task = PythonOperator(
        task_id="run_evidently_drift_check",
        python_callable=evaluate_data_drift
    )
```

---

## 6. Classroom Quiz Analysis & Conceptual Traps
- **Quiz ID**: `884296695175`.
- **Covariate Shift vs Concept Drift**:
  - *Covariate Shift*: The feature distribution $P(X)$ changes between training and production, but the conditional probability $P(Y \mid X)$ remains unchanged.
  - *Concept Drift*: The fundamental relationship $P(Y \mid X)$ changes over time (e.g. consumer spending patterns shift due to inflation), requiring model retraining even if input feature distributions appear stable.
