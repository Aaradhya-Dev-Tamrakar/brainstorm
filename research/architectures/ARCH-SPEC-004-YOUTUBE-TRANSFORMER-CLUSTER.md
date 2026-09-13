> **Artifact ID:** `ARCH-SPEC-004`  
> **Title:** Autonomous YouTube Cluster & Media Transformer Engine: Audience Seeding, Dynamic Lyrical Typography & Normal-to-Nightcore DSP Pipeline  
> **Version:** `1.0.0`  
> **Status:** `ACTIVE_SPECIFICATION`  
> **Principal Architect:** Aaradhya Dev Tamrakar  
> **Discipline:** Autonomous Media Pipelines, Digital Signal Processing (DSP) & Hardware Acceleration  
> **Domain:** Programmatic Video Synthesis, Multi-Worker Media Ingestion & YouTube Algorithm Engineering  
> **Created Date:** 2026-09-14  
> **Evidence Tier:** `FORMAL_ARCHITECTURE`  
> **Repository:** `F:\Aaradhya-Dev-Tamrakar\brainstorm`  
> **Execution Context:** Antigravity / Gemini Engine  
> **Upstream Trace:** [`ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md`](../../ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md), [`ARCH-SPEC-003-HEADLESS-ORCHESTRATION-SUBSTRATE.md`](ARCH-SPEC-003-HEADLESS-ORCHESTRATION-SUBSTRATE.md), [`F:\AaradhyaDT\yt-dlp-live`](file:///F:/AaradhyaDT/yt-dlp-live)  
> **Downstream Trace:** `F:\AaradhyaDT\yt-dlp-live\transformer`, `F:\AaradhyaDT\yt-dlp-live\render`, Capability Contract `tube-transformer.contract.json`  

---

## 1. Strategic Rationale & Algorithmic Cold-Start Invariant

### 1.1 The YouTube Cold-Start Dilemma
New algorithmic channels face an epistemic discovery barrier: zero historical click-through rate (CTR), zero subscriber seed data, and low impression allocation from the YouTube recommendation engine. Monolithic high-effort video creation without programmatic velocity leads to creator burnout before the recommendation engine establishes an audience graph.

### 1.2 The Two-Pronged Audience Seeding Wedge
To solve the cold-start problem, the cluster deploys two high-velocity programmatic content archetypes before activating specialized transformations:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           TIER 1: HIGH-VELOCITY AUDIENCE SEEDING                        │
├─────────────────────────────────────────────┬───────────────────────────────────────────┤
│         TRACK A: PROGRAMMATIC LYRICS        │        TRACK B: SENSORY KIDS EDUTAINMENT  │
├─────────────────────────────────────────────┼───────────────────────────────────────────┤
│ • High organic search intent (song queries) │ • High session duration & playlist looping│
│ • Low churn, high initial view counts       │ • Massive repetition retention (10x+ replays)
│ • Millisecond word-level subtitle bounce    │ • Simple SVG vector scenes & phonics loops│
│ • Long-tail SEO search indexing             │ • Zero linguistic barrier, global audience│
└─────────────────────────────────────────────┴───────────────────────────────────────────┘
                                              │ Established Channel Authority & Watch Time
┌─────────────────────────────────────────────▼───────────────────────────────────────────┐
│                    TIER 2: THE CORE ASSET ENGINE (TRANSFORMER CLUSTER)                  │
│  • Normal -> Nightcore DSP Transformer Engine (Pitch + Tempo + Sub-Harmonics)           │
│  • Syllable-Level Dynamic Substation Alpha (.ass) Typography                            │
│  • Dual-Format Output: 16:9 Landscape (Search) & 9:16 Vertical (Shorts Traffic Funnel)  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. End-to-End Cluster Architecture

```
                                  [ Audio / Lyric Ingestion ]
                                  (Public Domain / Free / Stems)
                                                │
                       ┌────────────────────────┴────────────────────────┐
                       ▼                                                 ▼
        [ Normal -> Nightcore DSP Engine ]               [ Alignment & Timing Engine ]
        • Rubberband Pitch/Tempo Stretch                 • WhisperX Word/Phoneme Timestamps
        • Sub-Bass Saturation (60 Hz punch)              • Syllable Split & Karaoke Generator
        • ITU-R BS.1770 (-14 LUFS leveling)              • SSA/ASS Script Compilation (.ass)
                       │                                                 │
                       └────────────────────────┬────────────────────────┘
                                                │ Transformed Audio + ASS Subtitles
                                                ▼
                                [ Hardware-Accelerated Compositor ]
                                • Intel Core Ultra 7 155H QuickSync (QSV)
                                • Encoders: h264_qsv / av1_qsv (Zero CPU Stall)
                                • Audio-Reactive Visualizer (FFmpeg showwaves/vectorscope)
                                • High-Contrast Vector Background (Kids/Nightcore Aesthetic)
                                                │
                                                ▼
                                    [ Validated Video Output ]
                                    (1080p60 / 4K MP4 Containers)
                                                │
                                                ▼
                                 [ Autonomous Dispatch & Relay ]
                                 • Scheduled Upload via YouTube Data API v3
                                 • RTMP Stream Broadcast via yt-dlp-live Relay Engine
                                 • SEO Metadata, Chapters & Thumbnail Injection
```

---

## 3. Subsystem Technical Specifications

### 3.1 Subsystem A: Normal -> Nightcore DSP Transformer Engine

Amateur nightcore suffers from harsh formants ("chipmunk artifacting") and hollow bass. The professional DSP pipeline enforces mathematical acoustic balancing:

$$\text{Pitch Ratio } (P) = 2^{\frac{\Delta \text{semitones}}{12}} \quad \text{where } \Delta \text{semitones} \in [2.0, 3.5]$$
$$\text{Tempo Ratio } (T) \in [1.12, 1.28]$$

1. **Time-Pitch Transformation (`librubberband`):**
   - Independent pitch scaling and tempo modification with formant compensation (`crispness=5`).
2. **Sub-Harmonic Bass Restoration:**
   - Because accelerating tempo thins low frequencies, a targeted low-shelf parametric EQ injects $+4.5 \text{ dB}$ at $60\text{ Hz}$ with $Q=0.8$ to maintain club/headphone punch.
3. **Mastering & Dynamic Loudness Invariant:**
   - Compliance with YouTube's broadcast normalization standard:
     $$\text{Integrated Loudness} = -14.0 \text{ LUFS} \pm 0.5 \text{ LUFS}$$
     $$\text{True Peak} \le -1.0 \text{ dBTP}$$
     $$\text{Loudness Range (LRA)} \le 7.0 \text{ LU}$$

### 3.2 Subsystem B: Dynamic Lyrical Typography & Alignment Engine

1. **Phonetic & Word-Level Timestamp Extraction:**
   - Local WhisperX / Wav2Vec2 forced alignment aligns raw transcript text against the audio waveform down to millisecond accuracy.
2. **Karaoke Script Synthesizer (`.ass` SSA Format):**
   - Generates Advanced Substation Alpha script files using inline karaoke timing tags `{\k<centiseconds>}`.
   - **Visual Profiles:**
     - **Nightcore Aesthetic:** Neon outer glow (`\3c&H00FFFF&`), active syllable scale pulse (`\fscx115\fscy115`), beat-synced particle drop.
     - **Kids Edutainment Aesthetic:** High-legibility rounded typography (e.g., Fredoka Bold), primary color switching, bouncing indicator glyph over active syllable.

### 3.3 Subsystem C: Hardware-Accelerated Video Compositor (Intel Arc QSV)

Workstation hardware is an **Intel Core Ultra 7 155H** (16 cores, 22 threads) with integrated **Intel Arc Graphics**. Rendering is offloaded directly to Intel QuickSync:

| Parameter | 16:9 Landscape Production | 9:16 Shorts / Viral Funnel |
|---|---|---|
| **Resolution** | $1920 \times 1080$ / $2560 \times 1440$ | $1080 \times 1920$ |
| **Framerate** | 60.0 fps | 60.0 fps |
| **Video Codec** | `h264_qsv` (broadest playback) or `av1_qsv` | `h264_qsv` |
| **Bitrate Control**| Lookahead VBR (8.5 Mbps target, 12 Mbps peak) | VBR (6.0 Mbps target) |
| **Audio Codec** | AAC-LC, 320 kbps, 48 kHz stereo | AAC-LC, 192 kbps, 48 kHz stereo |
| **Render Speed** | $\approx 15\times - 30\times$ real-time speed | $\approx 25\times - 40\times$ real-time speed |

### 3.4 Subsystem D: Content Schedulers & Autonomous Distribution

1. **Existing Module Integration:**
   - Connects directly to `F:\AaradhyaDT\yt-dlp-live`:
     - Uses `relay_live.ps1` for 24/7 RTMP looping / ambient radio live streams (e.g., "24/7 Nightcore Chill/Gaming Radio" or "24/7 Nursery Rhymes Loop").
     - Uses `record_live.ps1` to ingest reference audio streams and archive output broadcast quality.
2. **Metadata & Thumbnail Synthesis:**
   - Automated SEO description generation with clickable tracklist timestamps, copyright disclaimers, and algorithmic tag clouds.
   - Dual-thumbnail compilation (CTR-optimized typography overlay on primary color gradients).

---

## 4. Verification & Testing Matrix

```
┌────────────────────────┬───────────────────────────────────────────┬────────────────────────┐
│ TEST HARNESS           │ PASS CRITERIA                             │ VERIFICATION METHOD    │
├────────────────────────┼───────────────────────────────────────────┼────────────────────────┤
│ DSP Pitch/Tempo Audit  │ Delta Pitch = +2.5 st, No clipping        │ FFmpeg ebur128 + sox   │
│ Loudness Compliance    │ -14.0 LUFS +/- 0.5, TP <= -1.0 dBTP       │ ITU-R BS.1770 filter   │
│ Subtitle Alignment     │ Subtitle sync divergence <= 35 ms         │ Word boundary check    │
│ Hardware Acceleration  │ QSV hardware encoder engaged, CPU < 15%   │ intel_gpu_top / TaskMgr│
│ Container Integrity    │ Clean MP4 moov atom, valid sync markers   │ ffprobe container test │
└────────────────────────┴───────────────────────────────────────────┴────────────────────────┘
```

---

## 5. Architectural Contract: `tube-transformer.contract.json`

```json
{
  "$schema": "https://aaradhyadt.dev/schemas/capability.contract.v1.json",
  "module": "tube-transformer-cluster",
  "version": "1.0.0",
  "location": "F:\\AaradhyaDT\\yt-dlp-live",
  "tracking_branch": "yt-dlp-live",
  "runtime": "powershell7-python3.11",
  "capabilities": [
    {
      "id": "audio_transform_nightcore",
      "category": "dsp_audio_processing",
      "deterministic": true,
      "side_effects": true,
      "verification_tier": "empirical_benchmark",
      "inputs": {
        "source_audio": "string (filepath)",
        "pitch_shift_semitones": "number (default: 2.5)",
        "tempo_scale": "number (default: 1.20)",
        "bass_boost_db": "number (default: 4.5)",
        "target_lufs": "number (default: -14.0)"
      },
      "outputs": {
        "output_audio": "string (filepath)",
        "measured_lufs": "number",
        "sample_rate": "number"
      }
    },
    {
      "id": "generate_karaoke_subtitles",
      "category": "subtitles_and_alignment",
      "deterministic": true,
      "side_effects": true,
      "verification_tier": "empirical_benchmark",
      "inputs": {
        "source_audio": "string (filepath)",
        "transcript_text": "string | null",
        "style_preset": "nightcore_neon | kids_bubble"
      },
      "outputs": {
        "ass_subtitle_file": "string (filepath)",
        "aligned_word_count": "number"
      }
    },
    {
      "id": "compose_and_render_video",
      "category": "hardware_accelerated_render",
      "deterministic": true,
      "side_effects": true,
      "verification_tier": "empirical_benchmark",
      "inputs": {
        "audio_file": "string (filepath)",
        "subtitle_file": "string (filepath)",
        "background_visual": "string (filepath | procedural)",
        "orientation": "16:9 | 9:16",
        "encoder": "h264_qsv | av1_qsv"
      },
      "outputs": {
        "output_video_path": "string (filepath)",
        "render_fps": "number",
        "duration_seconds": "number"
      }
    }
  ]
}
```
