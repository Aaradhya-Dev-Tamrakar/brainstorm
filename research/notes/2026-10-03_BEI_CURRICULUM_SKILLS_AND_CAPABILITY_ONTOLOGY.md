# Master Curriculum Ontology: Engineering Competencies & Skills Architecture Derived from the 4-Year BE ECIE / BEIE Degree

- **Date:** 2026-10-03
- **Classification:** Epistemic Research Note & Capability Matrix (`ARCH-RFC-001` Compliant)
- **Status:** Ratified / Ground Truth Reference
- **Source Syllabus:** [`research/references/BEIE_Complete_Syllabus_I_to_IV.md`](../references/BEIE_Complete_Syllabus_I_to_IV.md)
- **Companion Transcripts:**
  - [`research/transcripts/2026-09-24_BEI-CAPABILITY-GAP-ANALYSIS_CONVERSATION.md`](../transcripts/2026-09-24_BEI-CAPABILITY-GAP-ANALYSIS_CONVERSATION.md)
  - [`research/notes/2026-10-02_ECOSYSTEM_SKILLS_AND_WORKFLOW_CALIBRATED_EVALUATION.md`](2026-10-02_ECOSYSTEM_SKILLS_AND_WORKFLOW_CALIBRATED_EVALUATION.md)
- **Ecosystem Implementation:** [`tools/skills/`](../../tools/skills/) | [`sim/bei_foundation_sim.py`](../../sim/bei_foundation_sim.py)

---

## 1. Executive Summary & Epistemic Framework

The Bachelor of Electronics, Communication and Information Engineering (BE ECIE / BEIE) curriculum across Tribhuvan University (IOE) comprises **51 degree-completion courses** (45 core courses, 3 electives, and 3 engineering design projects) selected from a total catalog of **73 accredited course syllabi**.

Historically, university engineering degrees are evaluated through paper examinations, creating an illusion of competency that degrades upon encountering messy, real-world distributed architectures. This document systematically deconstructs all 73 syllabi across 8 semesters, categorizing them into **10 Unified Engineering Domains**.

Under **`ARCH-RFC-001` Epistemic Governance**, every capability claim is calibrated across four tiers:
* `FORMALLY_PROVEN`: Mathematical theorems, Boolean algebra, automata, discrete structures, and SMT invariants.
* `EMPIRICALLY_VERIFIED`: Confirmed via deterministic code execution, Python test suites, and simulation harnesses (`sim/`).
* `STATISTICALLY_OBSERVED`: Supported by benchmark distributions, packet loss traces, and empirical signal metrics.
* `HEURISTIC_HYPOTHESIS`: Architectural conventions, agile workflows, and design heuristics.

---

## 2. Curriculum Architecture & Semester Breakdown

```
Semester 1 (I/I)   : 6 Core Subjects   [Calculus I, Drawing I, Basic Electrical, C Programming, Physics, Digital Logic]
Semester 2 (I/II)  : 6 Core Subjects   [Calculus II, Microprocessors, Chemistry, OOP in C++, Workshop, Circuits & Machines]
Semester 3 (II/I)  : 6 Core Subjects   [Math III (Transforms), EDC, Control Systems, Probability/Stats, Electromagnetics, Instrumentation]
Semester 4 (II/II) : 6 Core Subjects   [Applied Math, Discrete Structures, DSA, Advanced Electronics, Computer Graphics, Numerical Methods]
Semester 5 (III/I) : 6 Core Subjects   [Economics, DBMS, Networks, Computer Architecture, Operating Systems, Filter Design]
Semester 6 (III/II): 7 Subjects        [Comm English, Project Management, Propagation & Antenna, Comm Systems, OOSE, Embedded Systems, Minor Project]
Semester 7 (IV/I)  : 7 Subjects        [RF & Microwave, AI, Org & Management, DSP, Wireless Comms, Elective I (EX 725 04 Aero Telecom), Project Part A]
Semester 8 (IV/II) : 7 Subjects        [Telecommunications, Ethics & Law, Energy & Society, Information Systems, Elective II, Elective III, Project Part B]
-------------------------------------------------------------------------------------------------------------------------------------------------
TOTALS             : 51 Completed Units (45 Core Courses + 3 Electives + 3 Engineering Projects) from 73 Available Syllabi
```

---

## 3. The 10 Master Engineering Competency Domains

### Domain 1: Physical Foundations, Workshop Fabrication & Engineering Graphics
* **Coursework:** `ME 401` (Drawing I), `SH 402` (Physics), `SH 453` (Chemistry), `ME 453` (Workshop Technology).
* **Curriculum Hours:** 240 Contact Hours (Lectures + Drafting + Machine Shop Labs).
* **First-Principles Competencies (`EMPIRICALLY_VERIFIED`):**
  - Geometric Dimensioning & Tolerancing (GD&T): Orthographic projections, isometric views, sectioning planes, and standard fabrication tolerances.
  - Physical Wave Optics: Interference, diffraction gratings, polarization, Snell's law, numerical aperture ($NA$) in step-index optical fibers.
  - Solid-State Physics: Intrinsic vs. extrinsic semiconductor carrier concentration ($n_i^2 = n \cdot p$), Fermi-Dirac distribution, depletion layer mechanics.
  - Material Chemistry: Galvanic corrosion thermodynamics (Nernst equation), polymer dielectric breakdown, thermal heat dissipation.
  - Prototyping: Machining on lathes/mills, sheet metal bend deductions, enclosure ventilation, and PCB physical clearances.
* **Ecosystem Realization:** Physical edge-node hardware mounting, thermal budgeting for local AI compute rigs, and hardware enclosure design.
* **The Reality Gap:** Classroom drawing emphasizes manual pencil drafting; modern engineering demands parametric 3D CAD (FreeCAD/Fusion 360) and thermal finite element analysis (FEA).

---

### Domain 2: Electrical Circuits, Network Theory & Power Electronics
* **Coursework:** `EE 401` (Basic Electrical), `EE 460` (Electric Circuits & Machines), `EE 785.07` (Power Electronics - Elective III).
* **Curriculum Hours:** 210 Contact Hours (Theory + Machine Laboratories).
* **First-Principles Competencies (`FORMALLY_PROVEN` & `EMPIRICALLY_VERIFIED`):**
  - Network Theorems: Linear circuit solution via Kirchhoff's laws (KVL/KCL), Node-Voltage/Mesh-Current methods, Thevenin and Norton equivalents, and Maximum Power Transfer theorem ($Z_L = Z_{th}^*$).
  - AC Phasors & Resonance: Complex impedance ($Z = R + j\omega L - j/\omega C$), series/parallel resonance, quality factor ($Q = \omega_0 L / R$), and power factor correction ($\cos\theta$).
  - Transient Analysis: First and second-order differential equations for RL, RC, and RLC networks; zero-input and zero-state responses.
  - Electromechanics: Faraday's and Lenz's laws, magnetic flux linkage ($\Phi = B \cdot A$), mutual inductance, transformer turns ratio, induction motor torque-slip curves, and synchronous machines.
  - Power Electronics: SCR, MOSFET, and IGBT switching states; buck/boost DC-DC converter topologies; pulse-width modulated (PWM) inverter harmonics.
* **Ecosystem Realization:** Power delivery modeling, power supply decoupling for high-frequency embedded boards, and surge protection.
* **The Reality Gap:** Academic labs focus on ideal transformers and passive AC bridges; industrial embedded design requires modeling ESR, trace parasitic inductance, thermal derating, and switching regulator noise.

---

### Domain 3: Analog Electronics, Digital Logic & Instrumentation
* **Coursework:** `EX 401` (Digital Logic), `EX 501` (Electronic Devices & Circuits), `EX 510` (Instrumentation), `EX 553` (Advanced Electronics), `EX 725 03` (Biomedical Instrumentation - Elective I).
* **Curriculum Hours:** 345 Contact Hours.
* **First-Principles Competencies (`FORMALLY_PROVEN` & `EMPIRICALLY_VERIFIED`):**
  - Boolean Minimization: Truth table formulation, Karnaugh maps (2-5 variables), Quine-McCluskey tabular minimization, hazards and race conditions.
  - Sequential Logic: Flip-flop excitation tables (SR, JK, D, T), synchronous and asynchronous counters, shift registers, Mealy vs. Moore state machines.
  - Transistor Physics & Biasing: BJT hybrid-$\pi$ small-signal model, FET transconductance ($g_m$), common-emitter/source amplifier gain and input/output impedances.
  - Operational Amplifiers: Inverting, non-inverting, summing, and difference configurations; instrumentation amplifiers (3-op-amp topology); Sallen-Key active low-pass/high-pass filters; Schmitt trigger hysteresis; 555 astable/monostable multivibrators.
  - Transducers & Instrumentation: Wheatstone bridge balancing equations ($\Delta V \approx \frac{V_s}{4} \cdot \frac{\Delta R}{R}$), thermocouple Seebeck coefficients, LVDT position sensing, Piezoelectric charge generation, and Nyquist-Shannon ADC sampling quantization noise.
* **Derived Agent Skill:** [`electronics-circuit-synth`](../../tools/skills/electronics-circuit-synth/SKILL.md)
* **The Reality Gap:** Textbook problems assume ideal op-amps ($A_{OL} = \infty, R_{in} = \infty$); real-world circuits require compensation for input offset voltages, finite Gain-Bandwidth Product (GBWP), slew rate limits, and Common-Mode Rejection Ratio (CMRR).

---

### Domain 4: Microprocessors, Computer Architecture & Low-Level Hardware
* **Coursework:** `EX 452` (Microprocessors), `CT 603` (Computer Organization & Architecture), `CT 765.04` (Advanced Computer Architecture - Elective II).
* **Curriculum Hours:** 225 Contact Hours.
* **First-Principles Competencies (`FORMALLY_PROVEN` & `EMPIRICALLY_VERIFIED`):**
  - Microprocessor Internals: 8085/8086 register models (AX, BX, CX, DX, SP, BP, SI, DI, IP, Flags), segmented memory addressing, bus timing cycles (ALE, $\overline{\text{RD}}$, $\overline{\text{WR}}$), hardware interrupt cascades (8259 PIC), and programmable peripheral interfaces (8255 PPI).
  - Datapath & Control: Hardwired vs. microprogrammed control units, ALU bit-slice designs, Booth's signed multiplication algorithm, and IEEE 754 floating-point representation.
  - Pipelining & Hazard Resolution: 5-stage RISC instruction pipeline (IF, ID, EX, MEM, WB), structural hazards, data hazards (forwarding/bypassing), control hazards (delayed branch, dynamic branch prediction buffers).
  - Advanced Architecture: Superscalar execution, instruction shelving buffers, register renaming, out-of-order completion (Tomasulo's algorithm), memory hierarchy (L1/L2/L3 cache associativity, MESI coherence), and CC-NUMA architectures.
* **Ecosystem Realization:** Low-level PE binary parsing, opcode dissection, and execution artifact reconstruction in [`cyber-forensics`](../../tools/skills/cyber-forensics/SKILL.md).
* **The Reality Gap:** The curriculum spends extensive time on obsolete 8085/8086 instruction sets; modern systems require understanding x86-64, ARM64, and RISC-V architectures, memory fences, and speculative execution side-channels (Spectre/Meltdown).

---

### Domain 5: Embedded Systems, Real-Time Operating Systems (RTOS) & Firmware
* **Coursework:** `CT 655` (Embedded System), `CT 725 03` (Embedded Systems Design using ARM - Elective I), `EX 654` (Minor Project).
* **Curriculum Hours:** 180 Contact Hours.
* **First-Principles Competencies (`EMPIRICALLY_VERIFIED`):**
  - Microcontroller Hardware: 8051, Microchip PIC, Atmel AVR, and ARM Cortex-M architecture (NVIC, SysTick, memory-mapped peripheral registers).
  - Low-Level Bus Protocols: Bit-banging and hardware controller operation for UART (start/stop/parity), SPI (CPOL/CPHA modes), $I^2C$ (open-drain, ACK/NACK, 7-bit addressing), and CAN bus (differential signaling, arbitration).
  - Firmware Architecture: Non-blocking event-driven super-loops, Interrupt Service Routine (ISR) circular buffers, volatile memory qualification, and direct register bit manipulation.
  - Real-Time OS (FreeRTOS): Rate Monotonic Scheduling (RMS), Earliest Deadline First (EDF), context switching overhead, priority inversion mitigation via priority inheritance, mutexes, counting semaphores, and inter-task message queues.
* **Derived Agent Skill:** [`embedded-firmware-scaffold`](../../tools/skills/embedded-firmware-scaffold/SKILL.md)
* **The Reality Gap:** Academic labs often write blocking delays (`delay_ms()`); robust production firmware requires strict deterministic state machines, watchdog timer servicing, DMA memory transfers, and power-sleep state transitions.

---

### Domain 6: Systems Programming, Operating Systems & Concurrency
* **Coursework:** `CT 401` (Computer Programming), `CT 451` (Object Oriented Programming), `CT 612` (Operating System), `CT 725 06` (Operating System Advanced - Elective I).
* **Curriculum Hours:** 270 Contact Hours.
* **First-Principles Competencies (`FORMALLY_PROVEN` & `EMPIRICALLY_VERIFIED`):**
  - Memory Management & Pointers: Pointer arithmetic, stack vs. heap allocation, struct padding/alignment, dynamic memory allocation (`malloc`/`free`, `new`/`delete`), RAII resource lifecycles, and function pointer tables.
  - Object-Oriented Semantics: Dynamic dispatch, virtual method tables (`vtable`), multiple and virtual inheritance, copy/move constructors, template metaprogramming, and exception safety guarantees.
  - OS Internals & Process Management: Process Control Block (PCB), thread states, CPU scheduling (Round Robin, Multilevel Feedback Queue), POSIX system calls (`fork`, `exec`, `wait`, `pipe`), and shared memory IPC.
  - Concurrency & Synchronization: Mutual exclusion algorithms (Peterson's, Test-and-Set), mutexes, counting semaphores, condition variables, reader-writer locks, and race condition detection.
  - Deadlock Governance: Coffman conditions, resource allocation graphs, Banker's safety and resource-request algorithm, and deadlock detection/recovery.
  - Memory Virtualization: Paging, multi-level page tables, Translation Lookaside Buffer (TLB), page faults, working set models, and page replacement policies (FIFO, LRU, Second-Chance Clock).
  - Storage & Security: Inode file system architectures, disk arm scheduling (SSTF, SCAN), Windows NTFS Access Control Lists (ACLs) and security descriptors.
* **Derived Agent Skill:** [`systems-concurrency-harness`](../../tools/skills/systems-concurrency-harness/SKILL.md)
* **Ecosystem Realization:** Multi-agent concurrency isolation in [`agent-teams-orchestration`](../../tools/skills/agent-teams-orchestration/SKILL.md), NTFS security manipulation in [`win-vault`](../../tools/skills/win-vault/SKILL.md), and execution triage in [`cyber-forensics`](../../tools/skills/cyber-forensics/SKILL.md).
* **The Reality Gap:** Textbook examples operate on toy single-file C programs; production systems programming requires thread sanitizers, cache-line false sharing prevention, lock-free atomics, and cross-platform asynchronous runtimes.

---

### Domain 7: Algorithms, Data Structures, Discrete Math & Computer Graphics
* **Coursework:** `CT 551` (Discrete Structure), `CT 552` (Data Structure and Algorithms), `EX 554` (Computer Graphics).
* **Curriculum Hours:** 225 Contact Hours.
* **First-Principles Competencies (`FORMALLY_PROVEN` & `EMPIRICALLY_VERIFIED`):**
  - Asymptotic Analysis: Formal definitions of $O$, $\Omega$, $\Theta$; recurrence relation solving via the Master Theorem and recursion trees.
  - Fundamental Data Structures: Stacks, circular queues, singly/doubly/circular linked lists, skip lists, hash tables with open addressing/chaining.
  - Hierarchical Structures: Binary search trees (BST), self-balancing AVL trees (LL, RR, LR, RL rotations), Red-Black trees, B-trees, binary heaps, and priority queues.
  - Graph Algorithms: Breadth-First Search (BFS), Depth-First Search (DFS), topological sort, Dijkstra's single-source shortest path, Bellman-Ford, Kruskal's and Prim's Minimum Spanning Tree (MST).
  - Discrete Automata & Logic: Propositional and predicate calculus, direct/contradiction/induction proofs, relations and partial orderings, Deterministic and Non-deterministic Finite Automata (DFA/NFA), regular expressions, and context-free grammars.
  - Computer Graphics: Digital Differential Analyzer (DDA), Bresenham's line and midpoint circle algorithms, 2D/3D affine transformation matrices (translation, rotation, scaling, shear), homogeneous coordinates, Cohen-Sutherland line clipping, Z-buffer hidden surface removal, and Phong reflection/shading.
* **Derived Agent Skill:** [`dsa-complexity-optimizer`](../../tools/skills/dsa-complexity-optimizer/SKILL.md)
* **Ecosystem Realization:** Problem statement and solution harvesting in [`cp-archive-harvester`](../../tools/skills/cp-archive-harvester/SKILL.md), and knowledge graph traversal (BFS/DFS, community clustering, shortest path) in [`graphify`](../../tools/skills/graphify/SKILL.md).
* **The Reality Gap:** Academic algorithm questions test standard textbook implementations; real-world engineering requires cache-locality awareness, SIMD vectorization, memory-efficient bitsets, and large-scale graph databases.

---

### Domain 8: Signals & Systems, Digital Signal Processing (DSP) & Dynamic Control
* **Coursework:** `SH 501` (Engineering Mathematics III), `EX 509` (Control System), `EX 605` (Filter Design), `EX 710` (Digital Signal Analysis and Processing), `CT 725 04` (Image Processing - Elective I), `CT 785.08` (Speech Processing - Elective III).
* **Curriculum Hours:** 345 Contact Hours.
* **First-Principles Competencies (`FORMALLY_PROVEN` & `EMPIRICALLY_VERIFIED`):**
  - Integral Transforms: Continuous Laplace transform, Fourier series, Fourier transform, and discrete-time Z-transform with Region of Convergence (ROC) analysis.
  - Dynamic Feedback Control: Transfer function derivation, block diagram algebra, Mason's gain rule, time-domain transient metrics (peak overshoot $M_p$, rise time $t_r$, settling time $t_s$), Routh-Hurwitz stability criterion, Root Locus trajectories, frequency response (Bode magnitude/phase margins, Nyquist stability contour), and state-space representation ($\dot{x} = Ax + Bu, y = Cx + Du$).
  - Analog Filter Synthesis: Approximation theory (Butterworth maximally flat, Chebyshev equiripple, Elliptic, Bessel linear-phase), passive LC ladder networks, active RC topologies (Sallen-Key, Multiple Feedback, State-Variable), and frequency scaling/transformations.
  - Digital Signal Processing: Discrete Fourier Transform (DFT), Fast Fourier Transform (FFT: Radix-2 Decimation-in-Time and Decimation-in-Frequency), digital FIR filter design using windowing (Rectangular, Hamming, Hanning, Blackman), digital IIR filter design via Bilinear Transformation (with frequency pre-warping), and finite word-length limit cycles.
  - Multimedia Signals: 2D spatial convolution kernels (Gaussian blur, Sobel/Prewitt edge detectors), histogram equalization, morphological operations, Short-Time Fourier Transform (STFT), and Mel-Frequency Cepstral Coefficients (MFCC) for speech acoustics.
* **Derived Agent Skills:** [`dsp-signal-engine`](../../tools/skills/dsp-signal-engine/SKILL.md) & [`control-systems-sim`](../../tools/skills/control-systems-sim/SKILL.md)
* **Ecosystem Realization:** Audio feature extraction, spectral noise gating, and sensor time-series processing in `SPARK`.
* **The Reality Gap:** Academic DSP is solved analytically on paper with 4-point DFTs; production DSP requires real-time streaming buffers, overlap-add/overlap-save convolution, fixed-point Q15/Q31 arithmetic, and NEON/AVX2 vector instructions.

---

### Domain 9: RF, Microwave, Wireless, Antennas & Aeronautical Telecommunications
* **Coursework:** `EX 503` (Electromagnetics), `EX 653` (Propagation and Antenna), `EX 656` (Communication Systems), `EX 716` (RF & Microwave), `EX 715` (Wireless Communications), `EX 703` (Telecommunication), `EX 725 04` (Aeronautical Telecommunication - Elective I), `EX 725 01` (Radar Technology - Elective I), `EX 725 02` (Satellite Communication - Elective I), `EX 765.01` (Optical Fiber Comms - Elective II).
* **Curriculum Hours:** 450 Contact Hours.
* **First-Principles Competencies (`FORMALLY_PROVEN` & `EMPIRICALLY_VERIFIED`):**
  - Electromagnetic Wave Theory: Maxwell's equations in differential and integral forms, boundary conditions at material interfaces, uniform plane wave propagation in lossless/lossy media, skin depth, and Poynting vector power density ($S = E \times H$).
  - RF Transmission Lines & Impedance: Distributed parameter model ($R, L, G, C$), characteristic impedance ($Z_0 = \sqrt{L/C}$), propagation constant, voltage reflection coefficient ($\Gamma$), Voltage Standing Wave Ratio (VSWR), and Smith Chart single-stub impedance matching.
  - Antennas & Wave Propagation: Infinitesimal dipole radiation fields, radiation resistance ($R_{rad}$), antenna gain, directivity ($D$), effective aperture ($A_e = \frac{\lambda^2}{4\pi} D$), broadside and end-fire antenna arrays, Yagi-Uda arrays, horn antennas, parabolic reflectors, ground wave, tropospheric scatter, ionospheric sky wave critical frequency ($f_c$) and Maximum Usable Frequency (MUF), and the Friis Transmission Equation.
  - Modulation & Multiplexing: Analog modulation (AM DSB-SC/SSB, FM Carson's bandwidth rule), digital modulation (ASK, FSK, BPSK, QPSK, 16-QAM constellation diagrams), pulse modulation (PAM, PWM, PCM with A-law/$\mu$-law companding), and multiplexing (FDM, TDM, WDM).
  - Telecommunication Switching: Circuit/packet switching architectures, SS7 signaling protocols, traffic engineering, Erlang B formula (loss systems) and Erlang C formula (queuing systems), and Grade of Service (GoS).
  - Aeronautical Telecommunications & Avionics (`EX 725 04`):
    - CNS/ATM Systems: ICAO Doc 9750 global air navigation architecture, Aeronautical Fixed Telecommunication Network (AFTN), Aeronautical Telecommunication Network (ATN), AMHS data links.
    - Ground Navigation Aids: Non-Directional Beacon (NDB), VHF Omni-directional Radio Range (VOR) phase-comparison principle, Doppler VOR (DVOR) cardioid rotation, airborne VOR receivers, and siting criteria.
    - Precision Landing & Distance Measurement: Distance Measuring Equipment (DME) Gaussian pulse interrogation and reply pairs, echo suppression; Instrument Landing System (ILS) Localizer (horizontal guidance, 90/150 Hz DDM) and Glide Slope (vertical descent, 3-degree slope), marker beacons.
    - Radar & Surveillance: Primary Radar pulse range equation ($R_{max} = [\frac{P_t G^2 \lambda^2 \sigma}{(4\pi)^3 P_{min}}]^{1/4}$), Secondary Surveillance Radar (SSR), Monopulse SSR, Mode-S addressable transponders, Radar Data Processing Systems (RDPS), Automatic Dependent Surveillance-Broadcast (ADS-B), and Multilateration (MLAT) Time-Difference-of-Arrival (TDOA) hyperbolic positioning.
    - Satellite & Telemetry: Global Navigation Satellite Systems (GNSS: GPS L1/L2 C/A code, GLONASS), pseudorange equations, Inmarsat/Intelsat aeronautical mobile satellites, and Flight Data / Cockpit Voice Recorders (Black Box).
* **Derived Agent Skills:** [`avionic-telecom-analyzer`](../../tools/skills/avionic-telecom-analyzer/SKILL.md) & [`rf-link-budget-calc`](../../tools/skills/rf-link-budget-calc/SKILL.md)
* **The Reality Gap:** Textbook questions test link budget calculations under ideal free-space conditions; production RF and avionics engineering requires accounting for rain attenuation, multipath fading, Doppler frequency shifts, phased-array beamforming, and strict DO-178C / DO-254 safety certifications.

---

### Domain 10: Software Engineering, Data Architecture, Project Management, Economics & Professional Ethics
* **Coursework:** `CT 610` (DBMS), `CT 613` (Computer Networks), `CT 657` (Object Oriented Software Engineering), `CT 658` (Project Management), `CE 615` (Engineering Economics), `ME 708` (Organization & Management), `CE 752` (Engineering Professional Practice), `CT 751` (Information Systems), `CT 765.02` (Agile Software Development - Elective II), `CT 765.07` (Big Data Technologies - Elective II), `CT 785.04` (Enterprise Application Design - Elective III), `SH 655` (Communication English), `CT 710` (Artificial Intelligence), `EX 707 & Project Part B` (Major Engineering Design Project).
* **Curriculum Hours:** 495 Contact Hours.
* **First-Principles Competencies (`FORMALLY_PROVEN`, `EMPIRICALLY_VERIFIED`, & `HEURISTIC_HYPOTHESIS`):**
  - Database Management Systems: Relational algebra, SQL (DDL, DML, DCL), functional dependencies, schema normalization up to Boyce-Codd Normal Form (BCNF), indexing mechanics (B+ tree search and page splits, hash indexes), ACID transactions, Write-Ahead Logging (WAL), and Two-Phase Locking (2PL) serializability.
  - Computer Networks: OSI 7-layer vs. TCP/IP model, data link framing and Cyclic Redundancy Check (CRC-32) error detection, sliding window flow control (Go-Back-N, Selective Repeat), IPv4/IPv6 CIDR subnetting, link-state (OSPF/Dijkstra) and distance-vector (BGP/Bellman-Ford) routing, TCP 3-way handshake and connection teardown, TCP congestion control (AIMD, Slow Start), socket programming, and application protocols (DNS, HTTP/HTTPS, TLS).
  - Software Engineering & Architecture: Unified Process (UP) lifecycle (Inception, Elaboration, Construction, Transition), UML structural and behavioral modeling (Class, Object, Component, Deployment, Use Case, Sequence, Activity, Statechart diagrams), subsystem partitioning, dependency inversion, Gang of Four (GoF) design patterns, unit/integration/system testing strategies, and software quality metrics (cyclomatic complexity, cohesion, coupling).
  - Agile Methodologies: Scrum roles, sprint ceremonies, Kanban WIP limits, user story decomposition, Test-Driven Development (TDD), and continuous integration pipelines.
  - Project Management (PMBOK): Work Breakdown Structure (WBS) decomposition, Precedence Diagramming Method (PDM), Critical Path Method (CPM) and PERT forward/backward passes (calculating Early Start, Late Start, and Total Slack), Earned Value Management (EVM: Planned Value $PV$, Earned Value $EV$, Actual Cost $AC$, Cost Variance $CV$, Schedule Variance $SV$, CPI, SPI), risk management matrix (mitigation, avoidance, transfer, acceptance), and quality control charts.
  - Engineering Economics: Time value of money, cash-flow diagrams, compounding formulas, Net Present Value (NPV), Internal Rate of Return (IRR), Benefit-Cost Ratio ($B/C$), straight-line and MACRS depreciation, and project replacement analysis.
  - Professional Practice, Ethics & Law: Nepal Engineering Council (NEC) code of conduct, engineering contract law, tendering processes (FIDIC standards), intellectual property rights (patents, copyrights, trade secrets), tort liability, and environmental impact assessments.
  - Formal Engineering Communication: Technical report composition, executive summaries, research dossiers, oral project defense, and peer-review critiques.
  - Artificial Intelligence: Intelligent agent architectures, uninformed search (BFS, DFS, Uniform Cost Search), informed heuristic search ($A^*$, IDA*), adversarial search (Minimax with Alpha-Beta pruning), Constraint Satisfaction Problems (CSPs with AC-3), propositional and first-order logic resolution refutation, Perceptrons, Multilayer Feedforward Neural Networks, and backpropagation gradient descent.
* **Derived Agent Skills:**
  - [`oose-architecture-modeler`](../../tools/skills/oose-architecture-modeler/SKILL.md)
  - [`pm-workflow-orchestrator`](../../tools/skills/pm-workflow-orchestrator/SKILL.md)
* **Ecosystem Realization:**
  - `schemas/capability.contract.v1.json` & `schemas/ecosystem.registry.json` (formal OOSE capability contracts).
  - `github-workflow` (WBS issue anchoring, `- [ ]` task tracking, zero synthetic SHA invariants).
  - `sync.bat` & `audit.bat` (automated quality control, zero-discrepancy reconciliation).
  - `blog-writing-like-claude` & `build_report.bat` (calibrated formal technical writing and LaTeX dossier compilation).
* **The Reality Gap:** Academic coursework teaches software engineering and project management as bureaucratic textbook rituals; real-world engineering requires autonomous multi-agent coordination, git worktree isolation, automated CI/CD linting, and continuous deterministic verification.

---

## 4. The 10 Derived Agent Skills Inventory (`tools/skills/`)

To operationalize this academic foundation into autonomous developer workflows, the ecosystem provides **10 dedicated agent skills**:

| # | Skill Directory | Derived Coursework | Primary Capabilities | Companion Script / Harness |
| :-: | :--- | :--- | :--- | :--- |
| **1** | [`oose-architecture-modeler`](../../tools/skills/oose-architecture-modeler/SKILL.md) | `CT 657`, `CT 451`, `CT 765.02` | Mermaid UML diagrams, subsystem allocations, JSON capability contracts. | In-skill schema templates |
| **2** | [`pm-workflow-orchestrator`](../../tools/skills/pm-workflow-orchestrator/SKILL.md) | `CT 658`, `CE 615`, `ME 708` | WBS decomposition, CPM critical paths, `- [ ]` task issues, token budgeting. | In-skill PDM generator |
| **3** | [`dsa-complexity-optimizer`](../../tools/skills/dsa-complexity-optimizer/SKILL.md) | `CT 552`, `CT 551` | Asymptotic bounds ($O(1)$ to $O(2^n)$), optimal data structures, CP algorithms. | Complexity analyzer |
| **4** | [`systems-concurrency-harness`](../../tools/skills/systems-concurrency-harness/SKILL.md) | `CT 612`, `CT 401`, `CT 725 06` | Race condition auditing, Banker's deadlock avoidance, thread-safe queues. | In-skill sync scaffolds |
| **5** | [`dsp-signal-engine`](../../tools/skills/dsp-signal-engine/SKILL.md) | `EX 710`, `EX 605`, `SH 501` | FIR/IIR filter synthesis, FFT spectrum analysis, quantization simulation. | [`filter_synth.py`](../../tools/skills/dsp-signal-engine/scripts/filter_synth.py) |
| **6** | [`embedded-firmware-scaffold`](../../tools/skills/embedded-firmware-scaffold/SKILL.md) | `CT 655`, `EX 452`, `CT 725 03` | Bare-metal C HAL drivers, register bitmasks, ISR ring buffers, FreeRTOS tasks. | Driver header templates |
| **7** | [`control-systems-sim`](../../tools/skills/control-systems-sim/SKILL.md) | `EX 509` | Transfer functions, Root Locus, Bode stability margins, closed-loop PID tuning. | [`control_analyzer.py`](../../tools/skills/control-systems-sim/scripts/control_analyzer.py) |
| **8** | [`avionic-telecom-analyzer`](../../tools/skills/avionic-telecom-analyzer/SKILL.md) | `EX 725 04`, `EX 725 01`, `EX 703` | Multilateration TDOA solver, Radar Range Equation, VOR/DME/ILS geometries. | [`aero_calc.py`](../../tools/skills/avionic-telecom-analyzer/scripts/aero_calc.py) |
| **9** | [`rf-link-budget-calc`](../../tools/skills/rf-link-budget-calc/SKILL.md) | `EX 503`, `EX 653`, `EX 716`, `EX 715` | Friis path loss, antenna directivity, transmission line VSWR, Smith chart matching. | [`rf_calc.py`](../../tools/skills/rf-link-budget-calc/scripts/rf_calc.py) |
| **10** | [`electronics-circuit-synth`](../../tools/skills/electronics-circuit-synth/SKILL.md) | `EX 501`, `EX 553`, `EX 510`, `EE 401` | Op-amp active filters, transistor DC biasing, Schmitt triggers, 555 timers, Wheatstone bridges. | [`circuit_calc.py`](../../tools/skills/electronics-circuit-synth/scripts/circuit_calc.py) |

---

## 5. Deterministic Foundation Verification Harness (`sim/bei_foundation_sim.py`)

To eliminate speculative claims and enforce deterministic truth, [`sim/bei_foundation_sim.py`](../../sim/bei_foundation_sim.py) executes **8 mathematical verification engines** covering all curriculum domains:
1. **DSA & Graph Traversal**: Dijkstra shortest path and topological sorting on a Directed Acyclic Graph (DAG).
2. **Systems Concurrency**: Thread-safe bounded ring-buffer queue with mutex and condition variable synchronization.
3. **Discrete Mathematics & Automata**: Propositional truth-table evaluator and Deterministic Finite Automaton (DFA) state validator.
4. **Signal Processing & Numerical Math**: Fast Fourier Transform vs. Direct Discrete Fourier Transform equivalence ($\epsilon \le 10^{-12}$), and 4th-order Runge-Kutta (RK4) numerical ODE solver.
5. **Dynamic Control Systems**: 2nd-order closed-loop step response simulation verifying PID convergence to reference setpoint.
6. **Project Management (CPM/PERT)**: Forward and backward pass DAG analysis calculating Early Start, Late Start, Total Slack, and the Critical Path.
7. **Aeronautical Telecommunications**: Multilateration Time-Difference-of-Arrival (TDOA) hyperbolic positioning solver and Radar Range Equation calculation.
8. **Engineering Economics**: Discounted cash-flow Net Present Value (NPV) and Earned Value Management (EVM) variance and performance indices ($CV, SV, CPI, SPI$).

---

## 6. Authoritative Conclusion & Epistemic Standing

The BE ECIE / BEIE curriculum provides an extraordinarily comprehensive systems-engineering foundation spanning physical mechanics, solid-state electronics, microprocessor hardware, systems software, network protocols, signal analysis, aeronautical telecommunications, and engineering governance.

By anchoring each academic discipline to:
1. Demonstrable first-principles engineering capabilities,
2. Version-controlled ecosystem tools (`SPARK`, `Cyber-Forensics`, `Win-Vault`, `FLEET-001`, `github-workflow`),
3. 10 modular autonomous agent skills under `tools/skills/`, and
4. Deterministic simulation test suites in `sim/`,

the gap between classroom theoretical knowledge and production engineering mastery is completely closed.
