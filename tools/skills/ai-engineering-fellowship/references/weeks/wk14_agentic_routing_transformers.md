# Week 14: Transformers & Agentic Routing (BERT vs SLM)

---
relevancy_tier: GOLDEN_REFERENCE
mentor_score: 100/100
classroom_id: 871731817910
quiz_id: 855742171651
local_path: F:\FuseAIF2026\M4\WK14
github_repo: https://github.com/AaradhyaDT/fuseAiF_wk14_agentic_routing
---

## 1. Overview & Latency-Accuracy Pareto Analysis
- **Scenario**: Autonomous intent routing and multi-tool dispatch for complex multi-agent swarms.
- **Challenge**: Large models (70B+) have high inference latency (500–2,000 ms) and prohibitive costs for high-throughput front-door routing.
- **Experimental Trade-Off**:
  - **Part A (Encoder-Only)**: Fine-tuned ModernBERT / RoBERTa for deterministic intent classification (<15 ms latency, >96% accuracy).
  - **Part B (Small Language Models)**: LoRA parameter-efficient fine-tuning on sub-1B models (e.g. Qwen 0.5B/1.5B) for structured JSON intent + parameter extraction (<50 ms latency).

---

## 2. SOTA Industry Best Practices & Production Standards
- **LoRA Parameter-Efficient Fine-Tuning**: When fine-tuning SLMs for agentic routing, freeze base model weights and inject low-rank decomposition matrices ($r=8, \alpha=16$) into attention projections (`q_proj`, `v_proj`). This reduces trainable parameters by >98% while preventing catastrophic forgetting.
- **Structured JSON Intent Schema**: Enforce strict JSON output schemas via Pydantic or Outlines/vLLM guided decoding to guarantee 100% syntactically valid tool arguments.
- **Latency-Accuracy Pareto Frontier**: Route straightforward deterministic queries (e.g. "Check account balance") through the fast encoder router, and escalate ambiguous multi-turn queries to larger reasoning agents.

---

## 3. Mentor Evaluation & Quality Rating
- **Assignment Grade**: **100 / 100** ("Agentic Routing: Fine-Tuning Transformers for Intent Classification").
- **Quiz Score**: **20 / 20** ("Week 14 Quiz: Transformers, LLMs, and Foundational Models" — perfect score).
- **Execution Authenticity**: Cleanly modularized into `split/support_routing_partA_encoders_v2.ipynb` and `split/support_routing_partB_slms_v2.ipynb` with recorded benchmark JSONs (`encoder_results.json`, `slm_results.json`).

---

## 4. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directory**: [`F:\FuseAIF2026\M4\WK14`](file:///F:/FuseAIF2026/M4/WK14)
  - `support_routing.ipynb` — Complete notebook.
  - `split/` — Modularized Part A & Part B notebooks.
  - `docs/Week 14 Quiz_ Transformers, LLMs, and Foundational Models.pdf` — Quiz PDF.
- **GitHub Remote Fallback**:
  - `https://github.com/AaradhyaDT/fuseAiF_wk14_agentic_routing`
  - Clone: `gh repo clone AaradhyaDT/fuseAiF_wk14_agentic_routing`

---

## 5. Golden Implementation Snippets

### Hugging Face Transformer Sequence Classifier Fine-Tuning
```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments

def train_intent_router(train_dataset, eval_dataset, num_labels: int, model_id: str = "FacebookAI/roberta-base"):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSequenceClassification.from_pretrained(model_id, num_labels=num_labels)
    
    training_args = TrainingArguments(
        output_dir="./intent_router_ckpt",
        learning_rate=2e-5,
        per_device_train_batch_size=32,
        num_train_epochs=4,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        fp16=True
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )
    trainer.train()
    return model, tokenizer
```

---

## 6. Classroom Quiz Analysis & Conceptual Traps
- **Quiz ID**: `855742171651` (20/20).
- **Multi-Head Attention vs Single Head**: Multi-head attention projects Queries, Keys, and Values $h$ times with different linear projections into dimension $d_k = d_{\text{model}} / h$. This allows the model to jointly attend to information from different representation subspaces at different positions.
