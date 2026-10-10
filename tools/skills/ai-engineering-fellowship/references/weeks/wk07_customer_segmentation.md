# Week 7: Customer Segmentation & Unsupervised Clustering

---
relevancy_tier: CALIBRATED_REFERENCE
mentor_score: 93/100
fellowship_rating: 8.0/10
classroom_id: 855022397723
quiz_id: 855025195155
local_path: F:\FuseAIF2026\M2\WK7
github_repo: https://github.com/AaradhyaDT/fuseAiF_wk7_customer_segmentation
---

## 1. Overview & Dataset Context
- **Scenario**: Lead Data Analyst for a global retail company discovering natural customer personas from 500,000+ unlabeled raw transactions.
- **Dataset**: UCI Online Retail II (`Year 2010-2011` sheet).
- **Core Algorithms**: K-Means (Elbow + Silhouette, k-means++), Hierarchical Clustering (Ward, Complete, Average, Single dendrograms), and DBSCAN.
- **Deliverable**: `Week_7_Clustering_Assignment_executed.ipynb` with executive business narrative.

---

## 2. SOTA Industry Best Practices & Production Standards
- **RFM+ Feature Engineering**: Don't cluster raw transactional rows. Aggregate to customer level:
  - Recency ($R$): Days since last purchase relative to analysis cutoff.
  - Frequency ($F$): Count of unique orders placed.
  - Monetary ($M$): Total expenditure.
  - Extended: Average Basket Size, Return Rate, Inter-Purchase Interval, Category Ratios.
- **Robust Outlier Scaling**: Retail monetary spend follows a Pareto distribution (power law). Standard `StandardScaler` (mean/variance) is distorted by whale spenders. Use `RobustScaler` (median & interquartile range) or log-transform prior to clustering.
- **DBSCAN Parameter Selection**: Estimate $\epsilon$ using the **$k$-distance graph** ($k = 2 \cdot \text{dim} - 1$); the optimal $\epsilon$ corresponds to the sharp knee/elbow of the sorted distance plot.

---

## 3. Mentor Evaluation & Quality Rating
- **Assignment Grade**: **93 / 100** ("Week 7: Clustering Assignment").
- **Quiz Status**: Handed in ("Clustering Quiz Assignment").
- **Fellowship Rating**: **8.0 / 10** (Live on portfolio).
- **Mentor Feedback**: Excellent dendrogram cut justifications; clear operational marketing translation for identified clusters (Champions, At-Risk, Bargain Hunters, Inactive).

---

## 4. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directory**: [`F:\FuseAIF2026\M2\WK7`](file:///F:/FuseAIF2026/M2/WK7)
  - `Week_7_Clustering_Assignment_executed.ipynb` — Executed notebook.
  - `plots/` — Dendrograms, silhouette plots, and 3D cluster projections.
  - `misc/dev_artifacts/` — Intermediary feature tables.
- **GitHub Remote Fallback**:
  - `https://github.com/AaradhyaDT/fuseAiF_wk7_customer_segmentation`
  - Clone: `gh repo clone AaradhyaDT/fuseAiF_wk7_customer_segmentation`

---

## 5. Golden Implementation Snippets

### RFM Aggregation & DBSCAN Knee Estimation
```python
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

def compute_rfm_table(df: pd.DataFrame, snapshot_date: pd.Timestamp) -> pd.DataFrame:
    """Aggregate transaction logs into customer-level RFM features."""
    rfm = df.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda d: (snapshot_date - d.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("TotalSpend", "sum"),
        ReturnRate=("IsReturn", "mean")
    )
    return rfm

def estimate_dbscan_eps(X_scaled, min_samples: int = 5) -> np.ndarray:
    """Compute sorted k-distance for DBSCAN elbow heuristic."""
    nbrs = NearestNeighbors(n_neighbors=min_samples).fit(X_scaled)
    distances, _ = nbrs.kneighbors(X_scaled)
    k_distances = np.sort(distances[:, -1])
    return k_distances
```

---

## 6. Classroom Quiz Analysis & Conceptual Traps
- **Quiz ID**: `855025195155` (25 MCQs).
- **K-Means Sensitivity**: K-Means converges to local minima depending on initial centroid placement. Always use `init='k-means++'` with `n_init >= 10`.
- **DBSCAN Noise Handling**: In DBSCAN, points that do not satisfy core criteria ($|N_\epsilon(p)| \ge \text{MinPts}$) and are not within $\epsilon$ of a core point receive label `-1`. Never treat `-1` as a regular cluster.
