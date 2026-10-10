# Week 12: NLP & NER Sequence Labeling (CoNLL / WNUT)

---
relevancy_tier: GOLDEN_REFERENCE
mentor_score: 100/100
classroom_id: 871047207141
quiz_id: 871049299394
local_path: F:\FuseAIF2026\M3\WK12
github_repo: https://github.com/AaradhyaDT/fuseAiF_wk12_ner_customer_support
---

## 1. Overview & Business Setting
- **Scenario**: End-to-end Named Entity Recognition (NER) pipeline for customer support ticket routing.
- **Datasets**:
  - Primary: CoNLL-2003 (8,112 test tokens; PER, LOC, ORG, MISC).
  - Stress Test: WNUT-17 Emerging Entities (1,740 test tokens; novel surface forms).
- **Architecture**: `sklearn-crfsuite` Conditional Random Field (CRF) with rich lexical and contextual window features.
- **Results**: CoNLL-2003 micro-average **P 0.808 / R 0.806 / F1 0.807**; top class `I-PER` F1 0.911.

---

## 2. SOTA Industry Best Practices & Production Standards
- **Lexical & Contextual Feature Engineering**: Generate orthographic and neighboring token features without model bloat:
  - Token identity (lower, title, isupper, isdigit).
  - Prefix/suffix n-grams (lengths 1, 2, 3) to capture morphological word endings.
  - Directional neighbor context (tokens at $i-1$ and $i+1$, BOS/EOS boundaries).
- **The Out-of-Vocabulary (OOV) Reality Check (`INV-NER-OOV`)**: Standard benchmark scores (CoNLL F1 ~0.81) crash when encountering real-world emerging entities (WNUT-17 F1 dropped to 0.158, recall collapsed on corporations and creative works). Always design production pipelines to handle OOV tokens via subword representations or fallback dictionaries.
- **Business ROI Framing**: Translate raw F1 metrics into operational gains (e.g. projecting a 25% triage-time reduction via automated ticket routing).

---

## 3. Mentor Evaluation & Quality Rating
- **Assignment Grade**: **100 / 100** ("Assignment: NER Customer Support").
- **Quiz Score**: **20 / 20** ("W12: Natural Language Procession Quiz" — perfect score).
- **Execution Quality**: Commit `ebee7a7` verified on Google Colab; all 25 code cells executed sequentially with zero errors; concise 156-word business memo conforming to the 150–200 word spec.

---

## 4. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directory**: [`F:\FuseAIF2026\M3\WK12`](file:///F:/FuseAIF2026/M3/WK12)
  - `notebooks/Assignment3_NER_CustomerSupport.ipynb` — Executed notebook.
  - `docs/` — Error analysis write-ups.
- **GitHub Remote Fallback**:
  - `https://github.com/AaradhyaDT/fuseAiF_wk12_ner_customer_support`
  - Clone: `gh repo clone AaradhyaDT/fuseAiF_wk12_ner_customer_support`

---

## 5. Golden Implementation Snippets

### Contextual CRF Feature Extraction
```python
def word2features(sent, i):
    word = sent[i][0]
    features = {
        "bias": 1.0,
        "word.lower()": word.lower(),
        "word[-3:]": word[-3:],
        "word[-2:]": word[-2:],
        "word.isupper()": word.isupper(),
        "word.istitle()": word.istitle(),
        "word.isdigit()": word.isdigit(),
    }
    if i > 0:
        prev_word = sent[i - 1][0]
        features.update({
            "-1:word.lower()": prev_word.lower(),
            "-1:word.istitle()": prev_word.istitle(),
            "-1:word.isupper()": prev_word.isupper(),
        })
    else:
        features["BOS"] = True

    if i < len(sent) - 1:
        next_word = sent[i + 1][0]
        features.update({
            "+1:word.lower()": next_word.lower(),
            "+1:word.istitle()": next_word.istitle(),
            "+1:word.isupper()": next_word.isupper(),
        })
    else:
        features["EOS"] = True
    return features
```

---

## 6. Classroom Quiz Analysis & Conceptual Traps
- **Quiz ID**: `871049299394` (20/20).
- **Viterbi Decoding in CRFs**: Why is the Viterbi algorithm required for linear-chain CRFs?
  - *Answer*: Because entity transitions depend on neighboring labels, there are $K^T$ possible label sequences for a sentence of length $T$. Viterbi uses dynamic programming to find the exact globally optimal sequence in $O(T \cdot K^2)$ time.
