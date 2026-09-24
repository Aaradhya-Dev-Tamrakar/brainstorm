# Document 5: Academic, Fellowship & Edge Hardware Synergies

## 1. IOE Pulchowk / TU Engineering Coursework Integration
The ecosystem is deeply integrated with Aaradhya's Bachelor of Electronics, Communication, and Information Engineering (BEI) studies at Tribhuvan University (IOE Pulchowk / KEC).

### Core Mapped Coursework & Synergies
- **CT653: Artificial Intelligence**: State-space search, heuristics, game trees, logic formalization, and constraint satisfaction (implemented in `AI` Constraint Solver).
- **CT704: Digital Signal Analysis and Processing (DSP)**: Discrete transforms, FFT, filter design, and spectral analysis (directly mapped to `SPARK` kinematic accelerometer filtering and `yt-dlp-live` Nightcore audio DSP pipelines).
- **EX751: Wireless Communications**: Cellular network topologies, propagation models, fading channels, MIMO, and modulation schemes (aligned with `SPARK` BLE transmission protocol and `localsend-mcp` Wi-Fi communication).
- **EX752: RF and Microwave Engineering**: Transmission lines, Smith charts, impedance matching, waveguide propagation, S-parameters, and microwave planar circuit design.
- **EX725: Aeronautical Telecommunications**: Avionics navigation, radar systems, ADS-B telemetry, and VHF/UHF aviation communication standards.
- **ME708: Organization and Management**: Engineering economics, project lifecycle management, production planning, capital budgeting, and agile operational methodologies.

### Automated Academic Pipeline via Super-NLM & Classroom MCP
- **Google Classroom MCP**: Pulls real-time assignments, attachments, teacher stream announcements, and submission deadlines.
- **Super-NLM Course Sync (`auto_share_study_courses`)**: Automatically maps Semester 7 course materials across Google accounts and syncs course notebooks (CT653, CT704, EX751, EX752, EX725, ME708).

---

## 2. Fusemachines AI Fellowship 2026

- **Focus**: Advanced computer vision, NLP transformers, deep reinforcement learning, and production ML deployment.
- **Capstone & Research Audit**: Mapped in `BiasAperture` (demographic fairness auditing for computer vision models) and `SPARK` (two-layer edge AI wearable fall detection with SHAP explainability).
- **Audit Profile**: Rigorous benchmarking of disparity metrics across race, age, and gender slices with automated LaTeX research PDF generation.

---

## 3. Physical Fabrication & Embedded Edge Hardware

### SPARK Hardware Architecture
- **Microcontroller**: ESP32-S3 (Dual-core Xtensa LX7 @ 240MHz, 512KB SRAM, BLE 5.0).
- **Sensors**: 6-DoF Inertial Measurement Unit (IMU - Accelerometer + Gyroscope).
- **Edge Inference**: Two-layer hierarchical model. Layer 1 executes ultra-low-power kinematic thresholding on-chip; Layer 2 triggers deep sequence classification and SHAP attribution upon anomaly detection.

### Makerspace Prototyping Laboratory
- **CAD Modeling**: `fusion360-mcp` automates enclosure generation using exact ESP32-S3 PCB and battery physical tolerances.
- **Fabrication**: Bambu Studio slicer profiles, rapid PETG/PLA 3D printing, and modular wearable strap clips.
