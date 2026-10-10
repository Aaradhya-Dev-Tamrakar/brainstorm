# Week 1: Data Wrangling & Relational SQL Fundamentals

---
relevancy_tier: GOLDEN_REFERENCE
mentor_score: 100/100
classroom_id: 849624184865
quiz_id: 861655870837
local_path: F:\FuseAIF2026\M1\WK1
github_repo: https://github.com/AaradhyaDT/fuseAiF_wk1_data_wrangling
---

## 1. Overview & Theoretical Objectives
- **Scenario**: Data Scientist at a Regional Health Center.
- **Objective**: Ingest, clean, reconcile, and standardize patient health data across 3 fragmented operational databases (Administrative demographics, Laboratory results, and Lifestyle factors) to produce an analysis-ready dataset for downstream cardiac risk modeling.
- **Relational SQL Component**: Analyze retail transactions on the `classicmodels` relational database (8 tables: Customers, Products, Orders, OrderDetails, Payments, Employees, Offices, ProductLines).

---

## 2. SOTA Industry Best Practices & Production Standards
- **Contract-First Schema Assertion**: Use **Pandera** or Pydantic to validate column types, min/max range boundaries, and non-nullability constraints before running pipeline transformations.
- **Vectorized String Cleansing**: Replace slow Python string splits with vectorized Pandas `.str.extract()` with compiled regular expressions for parsing composite formats (e.g. `120/80 mmHg` into numeric `Systolic` and `Diastolic` integer columns).
- **Relational Integrity**: Enforce foreign key referential integrity checks during data extraction. Use `LEFT JOIN` with `IS NULL` filters to isolate orphaned records.
- **Deduplication Strategy**: When patient records are duplicated with slight timestamp variance, use window partition deduplication:
  ```sql
  WITH RankedVisits AS (
      SELECT *,
             ROW_NUMBER() OVER(PARTITION BY patient_id ORDER BY visit_date DESC) as rn
      FROM clinical_visits
  )
  SELECT * FROM RankedVisits WHERE rn = 1;
  ```

---

## 3. Mentor Evaluation & Quality Rating
- **Grade**: **100 / 100** (Full credit, on-time).
- **Quiz Status**: Handed in.
- **Mentor Commentary**: Strong data cleaning justifications in the exploratory notebook; comprehensive SQL queries demonstrating CASE statements, multi-table joins, and grouped aggregate metrics.

---

## 4. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directory**: [`F:\FuseAIF2026\M1\WK1`](file:///F:/FuseAIF2026/M1/WK1)
  - `Wk_1_Data_Wrangling_HeartAttack.ipynb` — Executed cleaning notebook.
  - `SQL_Assignment_Aaradhya.sql` — Completed SQL query suite.
  - `clean_patient_data.csv` — Standardized output dataset.
  - `mysqlsampledatabase (1).sql` — Seed script for `classicmodels`.
- **GitHub Remote Fallback**:
  - `https://github.com/AaradhyaDT/fuseAiF_wk1_data_wrangling`
  - Clone: `gh repo clone AaradhyaDT/fuseAiF_wk1_data_wrangling`

---

## 5. Key Implementation Snippets

### Blood Pressure Vectorized Cleansing
```python
import numpy as np
import pandas as pd

def clean_blood_pressure(df: pd.DataFrame, bp_col: str = "BloodPressure") -> pd.DataFrame:
    """Vectorized decomposition of string blood pressure readings."""
    pattern = r"^(?P<Systolic>\d{2,3})/(?P<Diastolic>\d{2,3})$"
    bp_parsed = df[bp_col].astype(str).str.extract(pattern).astype(float)
    
    # Anomaly bounds check (physiologically plausible limits)
    valid_mask = (
        bp_parsed["Systolic"].between(60, 260) & 
        bp_parsed["Diastolic"].between(40, 160) &
        (bp_parsed["Systolic"] > bp_parsed["Diastolic"])
    )
    bp_parsed[~valid_mask] = np.nan
    return pd.concat([df.drop(columns=[bp_col]), bp_parsed], axis=1)
```

---

## 6. Classroom Quiz Analysis & Conceptual Traps
- **Quiz ID**: `861655870837`
- **Trap 1: Imputation Order**: Imputing missing values *before* removing structural outliers contaminates the computed mean/median. Always prune extreme anomalies or use the median/IQR.
- **Trap 2: SQL Aggregation on NULLs**: `COUNT(column)` ignores `NULL` values, whereas `COUNT(*)` counts all rows. Using `AVG(salary)` divides only by rows where `salary IS NOT NULL`.
