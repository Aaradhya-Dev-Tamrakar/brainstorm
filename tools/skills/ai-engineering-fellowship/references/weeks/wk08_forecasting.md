# Week 8: Time Series Analysis & S&P 500 Forecasting

---
relevancy_tier: GOLDEN_REFERENCE
mentor_score: 100/100
fellowship_rating: 8.1/10
classroom_id: 855317094017
quiz_id: 868415924111
local_path: F:\FuseAIF2026\M2\WK8
github_repo: https://github.com/AaradhyaDT/fuseAiF_wk8_sp500_forecasting
---

## 1. Overview & Experimental Benchmark
- **Objective**: Rigorous classical-to-modern comparative benchmark across 9 individual forecasting models on the Monthly S&P 500 Index (1990–2024, 420 months).
- **Models Benchmarked**: Naïve, Seasonal-Naïve, Holt-Winters Exponential Smoothing, SARIMA, Prophet, LightGBM (recursive), LSTM, XGBoost, MLP.
- **Key Breakthrough**: A 4-model weighted ensemble (Holt-Winters + SARIMA + LSTM + XGBoost) achieved **MASE 2.44 / RMSE 96.7**, statistically outperforming all single models (confirmed via **Diebold-Mariano test: $p = 0.0092$**).

---

## 2. SOTA Industry Best Practices & Production Standards
- **Temporal Integrity**: Strictly forbid random K-Fold cross-validation on time series. Employ rolling-origin or expanding-window evaluation (`TimeSeriesSplit`).
- **Stationarity Protocol**: Jointly run **ADF** ($H_0$: Unit Root) and **KPSS** ($H_0$: Level/Trend Stationary) on log returns. Differencing order $d=1$ achieves stationary variance and mean.
- **Residual Ljung-Box Diagnostics**: Ensure SARIMA residuals are white noise across seasonal cycles:
  $$Q = n(n+2) \sum_{k=1}^h \frac{\hat{\rho}_k^2}{n - k} \sim \chi^2(h - p - q)$$
- **Ensemble Diversity**: Combine a statistical parametric model (Holt-Winters/SARIMA) with non-linear tree/deep models to smooth out individual model bias.

---

## 3. Mentor Evaluation & Quality Rating
- **Assignment Grade**: **100 / 100** ("Time Series and Forecasting Assignment").
- **Quiz Score**: **15 / 15** ("Time series and forecasting Quiz" — perfect score).
- **Fellowship Rating**: **8.1 / 10**.
- **Mentor Commentary**: Comprehensive residual analysis; rigorous Diebold-Mariano significance testing; clear investment-memo recommendation.

---

## 4. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directory**: [`F:\FuseAIF2026\M2\WK8`](file:///F:/FuseAIF2026/M2/WK8)
  - `assignment/sp500_sarima_v1.pkl` — Fitted SARIMA model pickle.
  - `docs/W8_Forecasting_Project_Guide.pdf` — Project guide.
  - `plots/` — 12 exported forecast, residual, and ACF/PACF figures.
- **GitHub Remote Fallback**:
  - `https://github.com/AaradhyaDT/fuseAiF_wk8_sp500_forecasting`
  - Clone: `gh repo clone AaradhyaDT/fuseAiF_wk8_sp500_forecasting`

---

## 5. Golden Implementation Snippets

### Diebold-Mariano Significance Test
```python
import numpy as np
from scipy import stats

def diebold_mariano_test(e1: np.ndarray, e2: np.ndarray, h: int = 1) -> float:
    """Diebold-Mariano test for equal predictive accuracy."""
    d = e1**2 - e2**2  # Squared error loss differential
    d_mean = np.mean(d)
    n = len(d)
    
    # Autocovariance adjustment for h > 1
    gamma0 = np.var(d, ddof=0)
    variance = gamma0
    for lag in range(1, h):
        gamma = np.mean((d[lag:] - d_mean) * (d[:-lag] - d_mean))
        variance += 2 * gamma
        
    dm_stat = d_mean / np.sqrt(variance / n)
    p_value = 2 * (1 - stats.norm.cdf(abs(dm_stat)))
    return float(p_value)
```

---

## 6. Classroom Quiz Analysis & Conceptual Traps
- **Quiz ID**: `868415924111` (15/15).
- **ACF vs PACF for Order Selection**:
  - AR($p$): ACF decays exponentially or as damped sinewave; PACF cuts off sharply after lag $p$.
  - MA($q$): PACF decays exponentially; ACF cuts off sharply after lag $q$.
