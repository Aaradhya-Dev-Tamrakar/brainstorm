# Research Profile & Technical Capability Summary
**Aaradhya Dev Tamrakar (ADT)**  
Final-Year B.E. in Electronics, Communication & Information Engineering (ECIE / BEI)  
Kathmandu Engineering College (KEC), Tribhuvan University | Expected Graduation: Jan 2027  
**Email:** aaradhyadevtmr@gmail.com | **Phone:** +977-9844602050 | **Location:** Kathmandu, Nepal  
**Portfolio:** [https://aaradhyadt.github.io](https://aaradhyadt.github.io) | **GitHub:** [https://github.com/AaradhyaDT](https://github.com/AaradhyaDT)

---

### Executive Summary: What I Deliver on Day 1
I am a systems and applied machine learning engineer specializing in the interface between **Edge AI firmware, sensor perception pipelines, and deterministic verification**. Rather than pure high-level prompt engineering or ungrounded simulations, I build end-to-end reproducible systems—from microsecond sensor interrupts on microcontroller silicon to quantized neural networks, SMT-backed formal verification, and automated evaluation harnesses.

---

### Core Technical Competencies

| Domain | Practical Capabilities & Tooling |
| :--- | :--- |
| **Deep Learning & Vision** | PyTorch, TensorFlow, OpenCV, INT8 Post-Training Quantization, ONNX, CNNs, Vision-Language OCR pipelines, SHAP explainability. |
| **Embedded & Autonomous Edge** | ESP-IDF (C/C++), FreeRTOS, ESP32-S3, IMU kinematics (MPU-6050 200 Hz ISR), UART/I2C/SPI bus protocol debugging. |
| **Formal Methods & Verification** | Z3 SMT Theorem Prover (SMT-LIB2), inductive invariant synthesis, state-machine bug discovery, AST-based consistency checkers. |
| **Systems & Data Engineering** | Python (FastAPI, SimPy, NumPy, Pandas), PostgreSQL, Docker sandboxing, Git automation workflows, Linux/Win32 systems. |

---

### Flagship Technical Artifacts

#### 1. SPARK — Wearable Edge AI Kinematics & Fall Detection Architecture
* **System:** Two-layer sensor architecture combining microsecond interrupt threshold gating on ESP32-S3 with edge neural classification and clinical SHAP explainability.
* **Empirical Results:** **18.5 KB INT8 quantized CNN** running on-chip; **0.9185 AUC-ROC** on SisFall dataset (38,420 temporal windows, subject-grouped zero-leakage cross-validation); 56 automated unit tests.
* **Significance:** Validates ability to compress and run real-time deep neural networks on constrained edge microcontrollers.

#### 2. Headless Invariant Assurance Engine (`INV-BMK-001`)
* **System:** Formal neurosymbolic verification harness translating system contracts into Z3 SMT constraints with containerized sandbox execution.
* **Empirical Results:** 12 evaluated properties across 4 state machines; **100% recall on planted violations**; **0.0% false discovery rate** on valid invariants; mean solver latency 18.3 ms.
* **Significance:** Demonstrates rigorous, zero-drift testing and formal proof methodology applied to software systems.

#### 3. BiasAperture — Algorithmic Fairness & Model Auditing Engine
* **System:** Statistical bias auditing framework evaluating deep vision and tabular classifiers, generating automated regulatory PDF audit certificates.
* **Empirical Results:** Audited 126 intersectional demographic bins using Disparate Impact Ratio and Equalized Odds Difference with BCa bootstrap confidence intervals.
* **Significance:** Proven capability in rigorous statistical evaluation, dataset curation, and reproducible reporting.

---

### Target Research Domains & Capabilities

* **Autonomous & Robotic Systems:** Multi-sensor fusion (LiDAR, radar, IMU, camera feeds), edge inference deployment on robotic/drone payloads, and real-time state estimation.
* **Applied AI & Computer Vision:** Deep learning vision pipelines, OCR text recognition for low-resource scripts and historical documents, and robust data preprocessing pipelines.
* **Smart Systems & Edge Intelligence:** End-to-end sensor-to-model integration, INT8 post-training model quantization for low-power edge microcontrollers, and automated telemetry pipelines.

---

### Academic & Fellowship Background
* **Fuse AI Fellowship (2026):** 14-week competitive fellowship in deep learning, machine learning systems, and agentic workflows (Fusemachines).
* **NSSR DataCamp Fellowship (Cohort 2):** Applied AI, PostgreSQL, and statistical data analysis (Nepalese Society of Student Researchers).
* **Leadership:** Vice Chair, IEEE KEC KTM Student Branch (2026–Present); Event Manager, Electronics Project Club.
