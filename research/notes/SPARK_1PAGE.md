# SPARK: Smart Protection & Alerting Resilient Kit
**One-Page Executive & Technical Research Summary**  
**Principal Architect:** Aaradhya Dev Tamrakar (Lead AI & Firmware Architect)  
**Academic Context:** B.E. Major Capstone Project (Electronics, Communication & Information Engineering)  
**Verification Tier:** `[EXPERIMENTALLY_VERIFIED]` (Evidence Tier E4) | **Status:** Functional Prototype  
**Repository / Portfolio:** [https://aaradhyadt.github.io](https://aaradhyadt.github.io)

---

### 1. Problem Statement & Challenge
Wearable fall detection systems for elderly and high-risk individuals suffer from a fundamental tension between **battery endurance** and **classification accuracy**. Continuous cloud offloading or running heavy models consumes prohibitive power and risks high latency, while simple accelerometer thresholding yields high false-alarm rates that lead to user abandonment.

---

### 2. Architectural Innovation: Two-Layer Hierarchical Gating

SPARK decouples microsecond kinematic event triggering from compute-intensive neural classification:

```text
[MPU-6050 6-DoF IMU] ──(200 Hz I2C)──> [ESP32-S3 Microcontroller]
                                                │
                                    [Layer 1: ISR Threshold Filter]
                                       │ (<50 µs response; zero overhead)
                                       ▼ (Trigger on kinematic anomaly)
                                    [Layer 2: INT8 Edge CNN Inference]
                                       │ (18.5 KB quantized network)
                                       ▼
                     [FastAPI Telemetry Hub & SHAP Clinical Explainability]
```

* **Layer 1 (Firmware Kinematics):** Continuous 200 Hz interrupt-service-routine (ISR) sampling on ESP32-S3 hardware via FreeRTOS. Power remains low until a threshold vector magnitude breach occurs.
* **Layer 2 (Quantized Edge Deep Learning):** A post-training quantized INT8 1D-CNN (18.5 KB footprint) runs strictly on-chip upon Layer 1 activation, classifying genuine falls versus activities of daily living (ADLs) in under 12 milliseconds.
* **Clinical Verification Layer:** When an event is logged, telemetry streams to a FastAPI service generating TreeSHAP and KernelSHAP feature-attribution visualizations, giving attending clinicians transparent interpretability over the trigger cause.

---

### 3. Quantitative Benchmarks & Empirical Proof

* **Neural Footprint:** Compressed to **18.5 KB INT8 weights**, fitting effortlessly into ESP32-S3 SRAM with zero external memory bus contention.
* **Classification Accuracy:** Achieved **0.9185 AUC-ROC** on the benchmark SisFall dataset across **38,420 temporal windows**.
* **Zero Data Leakage:** Evaluated via strictly subject-grouped cross-validation (training and test folds never share data from the same participant).
* **Test Suite:** 56 unit and integration tests verifying sensor bus communications, buffer sliding windows, inference precision, and alert dispatch.

---

### 4. Technical Transferability to Research Environments
* **Robotics & Autonomous Platforms:** High-frequency IMU/kinematics handling, interrupt-driven real-time embedded C++ firmware, and edge model optimization on constrained platforms.
* **Applied AI & Edge Intelligence:** Post-training model quantization, embedded runtime deployment, and full-stack sensor-to-dashboard telemetry pipelines.
