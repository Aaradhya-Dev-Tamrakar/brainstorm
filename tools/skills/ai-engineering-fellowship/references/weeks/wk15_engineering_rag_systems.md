# Week 15: Engineering AI Systems & Production RAG

---
relevancy_tier: CALIBRATED_REFERENCE
mentor_score: 86/100
classroom_id: 855838444105
quiz_id: 872358363656
local_path: F:\FuseAIF2026\M4\WK15
github_repo: https://github.com/AaradhyaDT/fuseAiF_wk15_ai_assistant_rag
---

## 1. Overview & Dual-Track Problem Set
- **Track 1 (Applied AI - RAG Assistant)**:
  - Connect to modern LLMs (OpenAI, Gemini, Anthropic).
  - Implement dynamic prompt engineering and structured JSON function calling.
  - Build RAG pipeline: document ingestion, semantic chunking, vector embeddings, vector DB.
  - Local serving via vLLM and full Docker containerization.
- **Track 2 (Engineering AI Systems - Productionizing Models)**:
  - Build interactive web UI (Streamlit).
  - Concurrency handling, latency optimization, rate limiting, and fallback model providers.

---

## 2. SOTA Industry Best Practices & Production Standards
- **Hybrid Dense-Sparse Search (`INV-HYBRID-RAG`)**: Pure vector search fails on keyword-specific queries (product codes, legal statute numbers). Combine dense semantic embeddings (`text-embedding-3-small` or BGE) with sparse BM25 keyword matching using Reciprocal Rank Fusion (RRF):
  $$\text{RRF}(d) = \sum_{m \in M} \frac{1}{60 + r_m(d)}$$
- **Cross-Encoder Reranking**: Retrieve top-25 candidate passages via hybrid search, then pass them through a cross-encoder (`bge-reranker-large`) to select the top-5 highest-precision chunks.
- **Production vLLM Deployment**: Serve open models with vLLM's PagedAttention engine to achieve 10–20x higher token throughput than naïve Hugging Face pipelines.

---

## 3. Mentor Evaluation & Quality Rating
- **Assignment Grade**: **86 / 100** ("W15 Assignment: Engineering AI Systems").
- **Quiz Status**: Handed in ("Applied AI and Engineering AI Systems").
- **Mentor Delta**: Solid containerization and pipeline; suggested deeper integration of automated retry circuit breakers and response caching (Redis semantic cache) for high-load resilience.

---

## 4. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directory**: [`F:\FuseAIF2026\M4\WK15`](file:///F:/FuseAIF2026/M4/WK15)
  - `W15_Assignment.md` — Problem set specification.
  - `README.md` — Project documentation.
- **GitHub Remote Fallback**:
  - `https://github.com/AaradhyaDT/fuseAiF_wk15_ai_assistant_rag`
  - Clone: `gh repo clone AaradhyaDT/fuseAiF_wk15_ai_assistant_rag`

---

## 5. Golden Implementation Snippets

### Production Hybrid RAG Retriever with Reranking
```python
from rank_bm25 import BM25Okapi

class ProductionRAGRetriever:
    def __init__(self, documents, vector_store, reranker=None):
        self.documents = documents
        self.vector_store = vector_store
        self.reranker = reranker
        self.tokenized_corpus = [doc.page_content.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def retrieve(self, query: str, top_k: int = 5):
        # 1. Sparse BM25 retrieval
        bm25_scores = self.bm25.get_scores(query.lower().split())
        bm25_top_idx = np.argsort(bm25_scores)[::-1][:20]
        
        # 2. Dense Vector retrieval
        dense_results = self.vector_store.similarity_search(query, k=20)
        
        # 3. Reciprocal Rank Fusion & Rerank
        candidates = list(set([self.documents[i] for i in bm25_top_idx] + dense_results))
        if self.reranker:
            pairs = [[query, c.page_content] for c in candidates]
            scores = self.reranker.compute_score(pairs)
            ranked_idx = np.argsort(scores)[::-1][:top_k]
            return [candidates[i] for i in ranked_idx]
        return candidates[:top_k]
```

---

## 6. Classroom Quiz Analysis & Conceptual Traps
- **Quiz ID**: `872358363656`.
- **Chunk Size vs Context Degradation**: Large chunks (>1,000 tokens) dilute semantic embedding sharpness; tiny chunks (<100 tokens) lose necessary conversational context. Use 300–500 token chunks with 50-token sliding overlap.
