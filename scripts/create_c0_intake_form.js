/**
 * Brainstorm Research Laboratory (BRL) — Cohort 0 Intake Form Generator
 * 
 * Instructions:
 * 1. Open https://script.google.com/
 * 2. Create a New Project: "BRL_Cohort_0_Intake_Generator"
 * 3. Paste this code into Code.gs
 * 4. Click "Run" -> select "createBRLCohort0Form"
 * 5. Grant permissions. The script will create the Form and log the edit URL and live URL!
 */

function createBRLCohort0Form() {
  const formTitle = "Brainstorm Research Laboratory — Cohort 0 Intake & Diagnostic";
  const form = FormApp.create(formTitle);
  
  form.setDescription(
    "Welcome to the Brainstorm Research Laboratory (BRL) Cohort 0 calibration fellowship.\n\n" +
    "BRL is an artifact-driven research collective focused on sovereign systems engineering, " +
    "formal verification, and reproducible technical outputs.\n\n" +
    "This diagnostic form collects baseline hardware, bandwidth, and quest preferences to match you " +
    "with your initial research quest.\n\n" +
    "Program Charter: PLAN-BRL-001\n" +
    "Laboratory Director: Aaradhya Dev Tamrakar"
  );
  form.setCollectEmail(true);
  form.setAllowResponseEdits(true);

  // -------------------------------------------------------------
  // SECTION 1: Identity & Access Configuration
  // -------------------------------------------------------------
  const sec1 = form.addSectionHeaderItem();
  sec1.setTitle("Section 1: Contributor Identity & System Access");
  sec1.setHelpText("Your GitHub username and Google account are required to provision repository and dataset access.");

  form.addTextItem()
    .setTitle("Full Name")
    .setRequired(true);

  form.addTextItem()
    .setTitle("College / Department / Current Semester")
    .setHelpText("e.g., Kathmandu Engineering College (KEC), Electronics & Computer Engineering, Semester 7")
    .setRequired(true);

  form.addTextItem()
    .setTitle("GitHub Username")
    .setHelpText("e.g., octocat (Do not include @)")
    .setRequired(true);

  form.addTextItem()
    .setTitle("Google Account Email")
    .setHelpText("Used for shared Google Drive datasets, Google Colab compute, and NotebookLM research engines.")
    .setRequired(true);

  // -------------------------------------------------------------
  // SECTION 2: Hardware & Environment Audit
  // -------------------------------------------------------------
  const sec2 = form.addPageBreakItem();
  sec2.setTitle("Section 2: Hardware & Execution Environment Audit");
  sec2.setHelpText("Helps us match you with quests suitable for your local machine or assign cloud compute (Colab) where needed.");

  form.addMultipleChoiceItem()
    .setTitle("Primary Operating System")
    .setChoiceValues([
      "Windows 11 / 10 (Native PowerShell)",
      "Windows Subsystem for Linux (WSL2 / Ubuntu)",
      "Linux (Native Ubuntu / Debian / Fedora / Arch)",
      "macOS (Apple Silicon M-series)",
      "macOS (Intel)"
    ])
    .setRequired(true);

  form.addTextItem()
    .setTitle("System RAM & CPU")
    .setHelpText("e.g., 16 GB RAM, AMD Ryzen 7 5800H (8 cores)")
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("Discrete Dedicated GPU Availability")
    .setChoiceValues([
      "NVIDIA RTX series (RTX 3060 / 4060 / etc.)",
      "NVIDIA GTX series (GTX 1650 / 1060 / etc.)",
      "Apple Silicon Unified Memory (M1/M2/M3/M4)",
      "Integrated Graphics Only (Intel Iris / AMD Radeon)",
      "Cloud Only (I plan to use Google Colab / Kaggle for compute)"
    ])
    .setRequired(true);

  form.addScaleItem()
    .setTitle("Git Command-Line Comfort")
    .setHelpText("1 = I rely on GitHub Desktop/UI; 5 = Comfortable with terminal git branch, rebase, cherry-pick")
    .setBounds(1, 5)
    .setLabels("GUI only", "Terminal native")
    .setRequired(true);

  // -------------------------------------------------------------
  // SECTION 3: Bandwidth & Calendar Alignment
  // -------------------------------------------------------------
  const sec3 = form.addPageBreakItem();
  sec3.setTitle("Section 3: Weekly Bandwidth & Exam Calendar");
  sec3.setHelpText("We operate on asynchronous, high-trust autonomy. Honesty regarding exam schedules prevents bottlenecking.");

  form.addMultipleChoiceItem()
    .setTitle("Realistic Committed Weekly Bandwidth")
    .setChoiceValues([
      "3 to 5 hours / week (Scout Pace)",
      "6 to 8 hours / week (Standard Fellowship Pace — Recommended)",
      "10+ hours / week (Intensive Track)"
    ])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("Upcoming Academic Blackout Dates (Exams, Vivas, Major Project Deadlines)")
    .setHelpText("List any weeks between October and December 2026 where you will be unavailable due to college exams or travel. (Write 'None' if free).")
    .setRequired(true);

  // -------------------------------------------------------------
  // SECTION 4: Quest Preferences & Skills Diagnostic
  // -------------------------------------------------------------
  const sec4 = form.addPageBreakItem();
  sec4.setTitle("Section 4: Research Quest Preferences (Cohort 0)");
  sec4.setHelpText("Select the research domains you are most motivated to investigate for your first sprint.");

  form.addMultipleChoiceItem()
    .setTitle("First-Choice Quest Preference")
    .setChoiceValues([
      "Quest C0-01: Discrete-Event Memory Simulator & Invariant Verification (Python, deterministic simulations)",
      "Quest C0-02: Nepal Public Authority Source Census & Accessibility Probing (Web data, TLS/HTTP, JSON schema)",
      "Quest C0-03: Devanagari Legacy Glyph Transcoding & Parallel Corpus (Unicode, font encodings, NLP)",
      "Quest C0-04: Tool Module Telemetry & Latency Profiling (Benchmarking, performance analysis)"
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("Second-Choice Quest Preference")
    .setChoiceValues([
      "Quest C0-01: Discrete-Event Memory Simulator & Invariant Verification",
      "Quest C0-02: Nepal Public Authority Source Census & Accessibility Probing",
      "Quest C0-03: Devanagari Legacy Glyph Transcoding & Parallel Corpus",
      "Quest C0-04: Tool Module Telemetry & Latency Profiling"
    ])
    .setRequired(true);

  // -------------------------------------------------------------
  // SECTION 5: Contributor Agreement & Governance Lock
  // -------------------------------------------------------------
  const sec5 = form.addPageBreakItem();
  sec5.setTitle("Section 5: BRL Governance & Contributor Agreement Sign-Off");
  sec5.setHelpText("Please review the core principles of the Brainstorm Research Laboratory.");

  const agreementText = 
    "By checking the boxes below, you affirm:\n\n" +
    "1. Permanent Attribution: All code, datasets, and reports authored by you will permanently bear your name and credit in Git history, release tags, and technical reports.\n" +
    "2. Tooling Boundary: BRL internal orchestration engines, 23-module capability mesh, and automation tools remain proprietary assets under BRL governance and will not be replicated or redistributed without permission.\n" +
    "3. Epistemic Rigor: Zero tolerance for fabricated citations, unverified AI halluncinations, or unrunnable code.\n" +
    "4. No-Guilt Pause: If coursework or exams become overwhelming, you agree to post [PAUSE] in the group to freeze your quest cleanly without guilt or penalty.";

  form.addCheckboxItem()
    .setTitle("Affirmation of BRL Contributor Agreement")
    .setHelpText(agreementText)
    .setChoiceValues([
      "I have read, understood, and accept the BRL Contributor Agreement (PLAN-BRL-001)."
    ])
    .setRequired(true);

  // Output Links
  Logger.log("=================================================");
  Logger.log("BRL Cohort 0 Intake Form Created Successfully!");
  Logger.log("Edit Form URL: " + form.getEditUrl());
  Logger.log("Published Live URL: " + form.getPublishedUrl());
  Logger.log("=================================================");
}
