#!/usr/bin/env python3
"""
Fusemachines AI Fellowship & AI Engineering Reference CLI Utility
Provides zero-token fast local queries, resolution checks, and curriculum navigation.
"""

import sys
import os
import argparse
from pathlib import Path

# Force UTF-8 encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

LOCAL_ROOT = Path(r"F:\FuseAIF2026")
GITHUB_PROFILE = "https://github.com/AaradhyaDT"

CURRICULUM = [
    {
        "week": 1,
        "topic": "Data Wrangling & SQL Fundamentals",
        "score": "100/100",
        "quiz": "Handed in",
        "tier": "GOLDEN_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M1\WK1",
        "repo": "fuseAiF_wk1_data_wrangling",
        "classroom_id": "849624184865",
        "sota": "Pandera schema validation, vectorized Pandas, window functions (ROW_NUMBER/RANK), CTEs, NULL-safe arithmetic",
        "key_files": ["Wk_1_Data_Wrangling_HeartAttack.ipynb", "SQL_Assignment_Aaradhya.sql", "mysqlsampledatabase (1).sql"],
    },
    {
        "week": 2,
        "topic": "Software Dev Concepts & FastAPI Microservice",
        "score": "75/100",
        "quiz": "Handed in",
        "tier": "CAUTIONARY_ANTI_PATTERN",
        "local_path": r"F:\FuseAIF2026\M1\WK2",
        "repo": "fuseAiF_wk2_customer_api_app",
        "classroom_id": "854212456010",
        "sota": "12-Factor App design, domain-based APIRouter separation, Pydantic v2 schemas, SQLAlchemy 2.0 async sessions, multi-stage Docker",
        "anti_pattern": "Monolithic single-file API penalized (-25 pts). Mandate: domain APIRouter in app/routers/, separate models/, db/, core/.",
        "key_files": ["main.py", "docker-compose.yml", "Dockerfile", "pyproject.toml"],
    },
    {
        "week": 3,
        "topic": "GenAI, Text-to-SQL & Agentic Query Execution",
        "score": "100/100",
        "quiz": "31/34",
        "tier": "GOLDEN_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M1\WK3",
        "repo": "fuseAiF_wk3_text2sql",
        "classroom_id": "864009032918",
        "sota": "AST visitor validation to block DML/DDL, context-aware schema pruning, 5-stage reflection loop, Pydantic JSON validation",
        "key_files": ["task1/", "task2/", "submission/"],
    },
    {
        "week": 4,
        "topic": "Statistical ML: Linear Models (Churn & CLV)",
        "score": "88/100",
        "quiz": "23/25",
        "tier": "CALIBRATED_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M1\WK4",
        "repo": "fuseAiF_wk4_linear_models",
        "classroom_id": "864517298853",
        "sota": "Strict in-fold scaler fitting (zero leakage), cost-utility decision threshold tuning (0.385 for top-200), VIF multicollinearity checks",
        "key_files": ["misc/outputs/"],
    },
    {
        "week": 5,
        "topic": "Tree Ensembles, SMOTE & SHAP Explainability",
        "score": "100/100",
        "quiz": "19/20",
        "tier": "GOLDEN_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M2\WK5",
        "repo": "fuseAiF_wk5_telco_churn_ensembles",
        "classroom_id": "854602584131",
        "sota": "imbalanced-learn ImbPipeline (SMOTE in training folds only), TreeSHAP exact computation, Joblib pipeline serialization, Model Cards",
        "key_files": ["misc/"],
    },
    {
        "week": 6,
        "topic": "Probabilistic Models & Bayesian Inference",
        "score": "100/100",
        "quiz": "20/20",
        "tier": "GOLDEN_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M2\WK6",
        "repo": "fuseAiF_wk6_probabilistic_models",
        "classroom_id": "798051144046",
        "sota": "PyMC 5.x MCMC sampling, Gelman-Rubin R-hat < 1.01 convergence diagnostics, prior/posterior predictive checks, GP kernel selection",
        "key_files": ["docs/W6_Probabilistic_Models_Resource_Guide.pdf"],
    },
    {
        "week": 7,
        "topic": "Customer Segmentation & Unsupervised Clustering",
        "score": "93/100",
        "quiz": "Handed in",
        "tier": "CALIBRATED_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M2\WK7",
        "repo": "fuseAiF_wk7_customer_segmentation",
        "classroom_id": "855022397723",
        "sota": "RobustScaler for skewed transactions, Hopkins clustering tendency, silhouette + Davies-Bouldin + Calinski-Harabasz, DBSCAN k-distance knee",
        "key_files": ["plots/", "misc/"],
    },
    {
        "week": 8,
        "topic": "Time Series Analysis & S&P 500 Forecasting",
        "score": "100/100",
        "quiz": "15/15",
        "tier": "GOLDEN_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M2\WK8",
        "repo": "fuseAiF_wk8_sp500_forecasting",
        "classroom_id": "855317094017",
        "sota": "Expanding-window temporal CV, ADF/KPSS joint stationarity, Ljung-Box residual checks, 4-model ensemble (MASE 2.44), Diebold-Mariano test (p=0.0092)",
        "key_files": ["assignment/", "docs/W8_Forecasting_Project_Guide.pdf", "plots/"],
    },
    {
        "week": 9,
        "topic": "Neural Network Foundations & NEU Defect CNN",
        "score": "100/100",
        "quiz": "Handed in",
        "tier": "GOLDEN_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M3\WK9",
        "repo": "fuseAiF_wk9_neu_defect_cnn",
        "classroom_id": "868825306318",
        "sota": "PyTorch from-scratch nn.Module, torchvision transforms, BatchNorm2d + Dropout(0.4), Optuna MedianPruner hyperparameter search",
        "key_files": ["data/NEU-DET/", "docs/resources/Neural Network Assignments - Classroom.pdf", "plots/"],
    },
    {
        "week": 10,
        "topic": "Classical Image Processing (OpenCV FreshTrack)",
        "score": "100/100",
        "quiz": "Handed in",
        "tier": "GOLDEN_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M3\WK10",
        "repo": "fuseAiF_wk10_image_processing",
        "classroom_id": "870378868125",
        "sota": "HSV color-space segmentation, morphological gradient outline, from-scratch Canny (96.9% agreement with cv2), Harris corners, Hough circles",
        "key_files": ["assignment/", "docs/"],
    },
    {
        "week": 11,
        "topic": "Vision Transformers, CLIP & Deep Learning CV",
        "score": "100/100",
        "quiz": "20/20",
        "tier": "GOLDEN_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M3\WK11",
        "repo": "fuseAiF_wk11_vision_transformers",
        "classroom_id": "870595309296",
        "sota": "ResNet-50 transfer learning, GradCAM, IoU & NMS from scratch, Faster R-CNN, DeepLabv3+, ViT patch embeddings, CLIP zero-shot (92.0%), ONNX export",
        "key_files": ["notebooks/W11_CV_Assignment_Notebook.ipynb", "docs/"],
    },
    {
        "week": 12,
        "topic": "NLP & NER Sequence Labeling (CoNLL / WNUT)",
        "score": "100/100",
        "quiz": "20/20",
        "tier": "GOLDEN_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M3\WK12",
        "repo": "fuseAiF_wk12_ner_customer_support",
        "classroom_id": "871047207141",
        "sota": "BIOES span labeling, sklearn-crfsuite CRF transition loss, WNUT-17 OOV entity stress testing, span-level F1 via seqeval, business ROI framing",
        "key_files": ["notebooks/Assignment3_NER_CustomerSupport.ipynb", "docs/"],
    },
    {
        "week": 13,
        "topic": "Sequence Learning & LSTM Text Classification",
        "score": "100/100",
        "quiz": "19/20",
        "tier": "GOLDEN_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M4\WK13",
        "repo": "fuseAiF_wk13_lstm_text_classification",
        "classroom_id": "871323847665",
        "sota": "PyTorch pack_padded_sequence, bidirectional LSTM recurrence, gradient clipping, embedding layer initialization",
        "key_files": ["LSTMs_for_Text_Classification.ipynb", "W13_ Sequence Learning Quiz.pdf"],
    },
    {
        "week": 14,
        "topic": "Transformers & Agentic Routing (BERT vs SLM)",
        "score": "100/100",
        "quiz": "20/20",
        "tier": "GOLDEN_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M4\WK14",
        "repo": "fuseAiF_wk14_agentic_routing",
        "classroom_id": "871731817910",
        "sota": "Encoder-only transformers (BERT/RoBERTa) vs SLMs (Qwen 0.5B/1.5B), LoRA/QLoRA parameter-efficient tuning, latency-accuracy Pareto frontier",
        "key_files": ["support_routing.ipynb", "docs/Week 14 Quiz_ Transformers, LLMs, and Foundational Models.pdf", "split/"],
    },
    {
        "week": 15,
        "topic": "Engineering AI Systems & Production RAG",
        "score": "86/100",
        "quiz": "Handed in",
        "tier": "CALIBRATED_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M4\WK15",
        "repo": "fuseAiF_wk15_ai_assistant_rag",
        "classroom_id": "855838444105",
        "sota": "Recursive semantic chunking, hybrid dense-sparse retrieval (BM25 + vector DB), re-ranking, vLLM local serving, Docker containerization",
        "key_files": ["W15_Assignment.md"],
    },
    {
        "week": 16,
        "topic": "Agentic Loop & Evaluation Harness",
        "score": "85/100",
        "quiz": "Handed in",
        "tier": "CALIBRATED_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M4\WK16",
        "repo": "fuseAiF_wk16_agentic_assistant",
        "classroom_id": "878032079298",
        "sota": "ReAct scratchpad state machines, context-window token budgeting, LLM-as-a-judge pairwise rubrics, deterministic evaluation harness",
        "key_files": ["LICENSE"],
    },
    {
        "week": 17,
        "topic": "Production MLOps (Dual Track: Churn + Agentic)",
        "score": "Turned In",
        "quiz": "Handed in",
        "tier": "GOLDEN_REFERENCE",
        "local_path": r"F:\FuseAIF2026\M5\WK17",
        "repo": "fuseAiF_wk17_telco_churn_mlops / fuseAiF_wk17_agentic_mlops",
        "classroom_id": "884301996556",
        "sota": "uv virtual environments, MLflow experiment tracking & model registry, Evidently AI data drift monitoring, FastAPI inference, Apache Airflow DAGs",
        "key_files": ["fuseAiF_wk17_agentic_mlops/", "fuseAiF_wk17_telco_churn_mlops/"],
    },
    {
        "week": 99,
        "topic": "Capstone: BiasAperture (Demographic Bias Audit)",
        "score": "Ecosystem #7",
        "quiz": "N/A",
        "tier": "GOLDEN_REFERENCE",
        "local_path": r"F:\FuseAIF2026\fuseai-fellowship\BiasAperture-A-Diagnostic-Framework-for-Demographic-Bias-Auditing-in-Facial-Analysis-",
        "repo": "BiasAperture",
        "classroom_id": "Capstone",
        "sota": "126 intersectional demographic bins, BCa bootstrap confidence intervals, disparate impact & equalized odds, automated LaTeX/PDF audit compliance",
        "key_files": ["pyproject.toml", "uv.lock"],
    },
]


def cmd_list(args):
    """Print complete curriculum summary table."""
    print("=" * 110)
    print(f"{'Wk':<4} {'Mentor':<9} {'Tier':<8} {'Topic':<36} {'Local Path':<24} {'GitHub Repo'}")
    print("=" * 110)
    for item in CURRICULUM:
        wk_str = f"W{item['week']:02d}" if item["week"] != 99 else "CAP"
        tier_short = item["tier"][:7]
        local_rel = str(Path(item["local_path"]).relative_to(LOCAL_ROOT)) if Path(item["local_path"]).is_relative_to(LOCAL_ROOT) else item["local_path"]
        print(f"{wk_str:<4} {item['score']:<9} {tier_short:<8} {item['topic'][:35]:<36} {local_rel:<24} {item['repo']}")
    print("=" * 110)
    print("Resolution Protocol: Local-First (F:\\FuseAIF2026) -> GitHub Remote Fallback (INV-RESOLVE-FUSE)")


def cmd_resolve(args):
    """Execute Local-First with GitHub Fallback resolution check."""
    wk = args.week
    matched = next((item for item in CURRICULUM if item["week"] == wk), None)
    if not matched:
        print(f"Error: Week {wk} not found in curriculum (1-17, 99 for Capstone).", file=sys.stderr)
        sys.exit(1)

    p = Path(matched["local_path"])
    print(f"--- Resolving Week {wk}: {matched['topic']} ---")
    if p.exists():
        print("  [LOCAL FOUND] Path exists on disk (Zero-latency fast path):")
        print(f"    Path: {p}")
        subfiles = list(p.glob("*"))[:8]
        print(f"    Contents ({len(list(p.glob('*')))} items):")
        for f in subfiles:
            prefix = "[DIR] " if f.is_dir() else "[FILE]"
            print(f"      {prefix} {f.name}")
    else:
        print("  [LOCAL NOT FOUND] Directory missing on this host:")
        print(f"    Target: {p}")
        print("  [FALLBACK] Use remote GitHub repository:")
        for r in matched["repo"].split(" / "):
            print(f"    Clone: gh repo clone AaradhyaDT/{r.strip()}")
            print(f"    URL:   {GITHUB_PROFILE}/{r.strip()}")


def cmd_lookup(args):
    """Full-text search across topics, SOTA best practices, and anti-patterns."""
    kw = args.keyword.lower()
    matches = []
    for item in CURRICULUM:
        haystack = f"{item['topic']} {item['sota']} {item.get('anti_pattern', '')} {item['repo']}".lower()
        if kw in haystack:
            matches.append(item)

    if not matches:
        print(f"No modules matched query '{args.keyword}'.")
        return

    print(f"Found {len(matches)} matching module(s) for '{args.keyword}':\n")
    for item in matches:
        wk_str = f"Week {item['week']}" if item["week"] != 99 else "Capstone (BiasAperture)"
        print(f"[{wk_str}] {item['topic']} | Mentor: {item['score']} ({item['tier']})")
        print(f"  Local:    {item['local_path']}")
        print(f"  GitHub:   {GITHUB_PROFILE}/{item['repo']}")
        print(f"  SOTA:     {item['sota']}")
        if "anti_pattern" in item:
            print(f"  WARNING:  {item['anti_pattern']}")
        print()


def cmd_week(args):
    """Print full dossier for a specific week."""
    wk = args.week
    item = next((i for i in CURRICULUM if i["week"] == wk), None)
    if not item:
        print(f"Error: Week {wk} not found.", file=sys.stderr)
        sys.exit(1)

    wk_str = f"Week {item['week']}" if item["week"] != 99 else "Capstone"
    print(f"=== {wk_str}: {item['topic']} ===")
    print(f"Mentor Score:      {item['score']}")
    print(f"Classroom Quiz:    {item['quiz']}")
    print(f"Relevancy Tier:    {item['tier']}")
    print(f"Classroom ID:      {item['classroom_id']}")
    print(f"Local Path:        {item['local_path']}")
    print(f"GitHub Fallback:   {GITHUB_PROFILE}/{item['repo']}")
    print("\n[SOTA Best Practice]")
    print(f"  {item['sota']}")
    if "anti_pattern" in item:
        print("\n[Mentor Anti-Pattern Warning]")
        print(f"  {item['anti_pattern']}")
    print("\n[Key Artifacts]")
    for kf in item.get("key_files", []):
        print(f"  - {kf}")


def main():
    parser = argparse.ArgumentParser(description="Fusemachines AI Fellowship Curriculum & Reference CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    subparsers.add_parser("list", help="List all 17 weeks and capstone with scores and tiers")

    # resolve
    p_res = subparsers.add_parser("resolve", help="Test local vs GitHub fallback resolution for a week")
    p_res.add_argument("week", type=int, help="Week number (1-17, 99 for Capstone)")

    # lookup
    p_look = subparsers.add_parser("lookup", help="Search curriculum by concept or keyword")
    p_look.add_argument("keyword", type=str, help="Search term (e.g. 'FastAPI', 'SMOTE', 'RAG')")

    # week
    p_wk = subparsers.add_parser("week", help="View full metadata for a specific week")
    p_wk.add_argument("week", type=int, help="Week number (1-17, 99 for Capstone)")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "resolve":
        cmd_resolve(args)
    elif args.command == "lookup":
        cmd_lookup(args)
    elif args.command == "week":
        cmd_week(args)


if __name__ == "__main__":
    main()
