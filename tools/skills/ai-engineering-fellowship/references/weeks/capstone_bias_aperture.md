# Capstone Project: BiasAperture (Demographic Vision Bias Audit)

---
relevancy_tier: GOLDEN_REFERENCE
mentor_score: Ecosystem Module #7
local_path: F:\FuseAIF2026\fuseai-fellowship\BiasAperture-A-Diagnostic-Framework-for-Demographic-Bias-Auditing-in-Facial-Analysis-
github_repo: https://github.com/AaradhyaDT/BiasAperture
ecosystem_branch: BiasAperture
---

## 1. Overview & Research Scope
- **Project**: BiasAperture — Diagnostic Framework for Demographic Bias Auditing in Facial Analysis Models.
- **Role in Ecosystem**: Official Ecosystem Module #7 (Aaradhya's Personal Tool Ecosystem Registry).
- **Team**: Aaradhya Dev Tamrakar & Tisha Manandhar.
- **Core Mission**: Automated statistical disparity auditing and regulatory compliance verification across deployed computer vision classifiers. The framework is strictly diagnostic: it rigorously measures and certificates disparities without modifying or retraining the audited model.

---

## 2. SOTA Industry Best Practices & Production Standards
- **Intersectional Demographic Binning (`INV-INTERSECT-BINS`)**: Never audit protected attributes (e.g. Gender, Age, Ethnicity) in isolation. Marginal parity masks acute intersectional penalties. BiasAperture slices performance across **126 mutually exclusive intersectional bins** (e.g., *Dark-Skinned Female Age 18–30*).
- **BCa Bootstrap Confidence Intervals**: Compute Bias-Corrected and Accelerated (BCa) bootstrap confidence intervals ($\ge 1,000$ resamples) on all parity metrics (Disparate Impact, Equal Opportunity, False Positive Rate Parity) to prevent false statistical significance alarms on small demographic cohorts.
- **Automated PDF/LaTeX Regulatory Compliance**: Compile automated regulatory audit certificates (EU AI Act & EEOC compliant) using Pandera validated schemas and LaTeX templates.

---

## 3. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directories**:
  - Fellowship Workspace: [`F:\FuseAIF2026\fuseai-fellowship\BiasAperture-A-Diagnostic-Framework-for-Demographic-Bias-Auditing-in-Facial-Analysis-`](file:///F:/FuseAIF2026/fuseai-fellowship)
  - Dedicated Ecosystem Repo: [`F:\Aaradhya-Dev-Tamrakar\BiasAperture`](file:///F:/Aaradhya-Dev-Tamrakar/BiasAperture)
- **GitHub Remote Fallback**:
  - `https://github.com/AaradhyaDT/BiasAperture`
  - Clone: `gh repo clone AaradhyaDT/BiasAperture`

---

## 4. Golden Implementation Snippets

### BCa Bootstrap Confidence Interval Calculation
```python
import numpy as np
from scipy import stats

def bca_bootstrap_metric(y_true, y_pred, metric_fn, n_resamples: int = 1000, alpha: float = 0.05):
    """Compute Bias-Corrected and Accelerated (BCa) confidence intervals."""
    n = len(y_true)
    theta_hat = metric_fn(y_true, y_pred)
    
    # 1. Bootstrap resamples
    boot_indices = np.random.randint(0, n, size=(n_resamples, n))
    theta_boot = np.array([metric_fn(y_true[idx], y_pred[idx]) for idx in boot_indices])
    
    # 2. Bias-correction parameter z0
    z0 = stats.norm.ppf(np.mean(theta_boot < theta_hat))
    
    # 3. Acceleration parameter 'a' via jackknife
    jack_values = np.zeros(n)
    for i in range(n):
        idx = np.delete(np.arange(n), i)
        jack_values[i] = metric_fn(y_true[idx], y_pred[idx])
    jack_mean = np.mean(jack_values)
    num = np.sum((jack_mean - jack_values)**3)
    denom = 6.0 * (np.sum((jack_mean - jack_values)**2)**1.5)
    a = num / denom if denom != 0 else 0.0
    
    # 4. Adjusted percentiles
    z_alpha = stats.norm.ppf(alpha / 2)
    z_1_alpha = stats.norm.ppf(1 - alpha / 2)
    
    pct_lower = stats.norm.cdf(z0 + (z0 + z_alpha) / (1 - a * (z0 + z_alpha))) * 100
    pct_upper = stats.norm.cdf(z0 + (z0 + z_1_alpha) / (1 - a * (z0 + z_1_alpha))) * 100
    
    ci_lower = np.percentile(theta_boot, pct_lower)
    ci_upper = np.percentile(theta_boot, pct_upper)
    return theta_hat, (ci_lower, ci_upper)
```

---

## 5. Architectural Invariants
- **INV-DIAGNOSTIC-ONLY**: BiasAperture measures and reports disparities; it never injects synthetic perturbations into the inference pipeline during an audit.
- **INV-AUDIT-REPRODUCIBLE**: All audit runs output a cryptographic manifest (SHA-256 hash of dataset, model weights, and hyperparameter config).
