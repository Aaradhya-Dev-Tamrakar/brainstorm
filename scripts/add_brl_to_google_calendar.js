/**
 * 1-Click Google Calendar Generator for BRL Cohort 0
 * 
 * Instructions:
 * 1. Go to https://script.google.com/
 * 2. Click "New Project"
 * 3. Paste this script into Code.gs
 * 4. Click "Run" -> select "addBRLCohort0Calendar"
 * 5. Review & Grant Calendar permissions.
 * 
 * Result: Automatically creates a dedicated secondary calendar:
 * "Brainstorm Research Lab — Cohort 0"
 * with all 5 milestone events populated with exact dates, times, and descriptions!
 */

function addBRLCohort0Calendar() {
  const calName = "Brainstorm Research Lab — Cohort 0";
  
  // Check if calendar already exists
  const existingCals = CalendarApp.getCalendarsByName(calName);
  let cal;
  if (existingCals.length > 0) {
    cal = existingCals[0];
    Logger.log("Found existing calendar: " + cal.getName());
  } else {
    cal = CalendarApp.createCalendar(calName, {
      summary: "Milestones, sprint deadlines, and reviews for BRL Cohort 0.",
      timeZone: "Asia/Kathmandu",
      color: CalendarApp.Color.BLUE
    });
    Logger.log("Created new secondary calendar: " + cal.getName());
  }

  const milestones = [
    {
      title: "🚀 [BRL C0] Milestone 1: Program Kickoff & Quest 0 (Dry-Run PR)",
      start: new Date("2026-10-05T15:00:00+05:45"),
      end: new Date("2026-10-05T17:00:00+05:45"),
      location: "KEC Makerspace / Google Meet Hybrid",
      description: "Brainstorm Research Laboratory Cohort 0 Kickoff:\n\n" +
                   "1. Distribution of BRL Contributor Agreement.\n" +
                   "2. Verification of local development setups & Git credentials.\n" +
                   "3. Submission and merge of Quest 0 (c0/<username>/quest-0).\n" +
                   "4. Unlocking of Rank E (Research Scout) standing.\n\n" +
                   "Charter: PLAN-BRL-001 | Spec: BRL_QUEST_0_DRY_RUN.md"
    },
    {
      title: "🔬 [BRL C0] Milestone 2: Sprint 1 Quest Assignment & Baseline Run",
      start: new Date("2026-10-12T15:00:00+05:45"),
      end: new Date("2026-10-12T16:30:00+05:45"),
      location: "KEC Makerspace / Async GitHub",
      description: "Execution of Sprint 1 research quests:\n\n" +
                   "• C0-01: Discrete-Event Memory Simulator reproduction.\n" +
                   "• C0-02: Nepal Public Authority source census.\n" +
                   "• C0-03: Devanagari legacy font transcoding vectors.\n" +
                   "• C0-04: Tool module telemetry profiling.\n\n" +
                   "Sync Gate: Initial commit on isolated feature branches."
    },
    {
      title: "⚖️ [BRL C0] Milestone 3: Mid-Cycle Review & Dual-Layer Audit Gate",
      start: new Date("2026-10-26T15:00:00+05:45"),
      end: new Date("2026-10-26T17:00:00+05:45"),
      location: "KEC Makerspace / Kupondole Hub",
      description: "Mid-Cycle progress review and technical gate check:\n\n" +
                   "1. Execution of .\\audit.bat across all active PRs.\n" +
                   "2. Peer review of collected datasets and simulation logs.\n" +
                   "3. Academic blackout check: Exam calendar synchronization.\n" +
                   "4. Grade rubric evaluation (Target: Score >= 8/15 for Rank D advancement)."
    },
    {
      title: "🛡️ [BRL C0] Milestone 4: Sprint 2 Edge-Case Probing & Invariant Check",
      start: new Date("2026-11-09T15:00:00+05:45"),
      end: new Date("2026-11-09T16:30:00+05:45"),
      location: "Async GitHub / KEC Makerspace",
      description: "Advancement into edge-case analysis:\n\n" +
                   "• Invariant violation probes (planted bugs / negative controls).\n" +
                   "• Devanagari ligature corner-cases (reph, nukta, half-forms).\n" +
                   "• Cross-platform reproducibility confirmation (Windows vs Linux)."
    },
    {
      title: "🎓 [BRL C0] Milestone 5: Final Artifact Delivery, Retrospective & Rank Promotion",
      start: new Date("2026-11-23T15:00:00+05:45"),
      end: new Date("2026-11-23T17:30:00+05:45"),
      location: "KEC Makerspace / Virtual Retrospective",
      description: "Cohort 0 Graduation & Artifact Ledgering:\n\n" +
                   "1. Final PR merge into main with zero audit discrepancies.\n" +
                   "2. Formal publication of BRL Cohort 0 Technical Report.\n" +
                   "3. Issuance of permanent cryptographic authorship credentials.\n" +
                   "4. Cohort 0 Retrospective: Pedagogical teaching tax & calibration for Cohort 1."
    }
  ];

  milestones.forEach(function(m) {
    const events = cal.getEvents(m.start, m.end, { search: m.title });
    if (events.length === 0) {
      cal.createEvent(m.title, m.start, m.end, {
        description: m.description,
        location: m.location
      });
      Logger.log("Added milestone: " + m.title);
    } else {
      Logger.log("Milestone already exists: " + m.title);
    }
  });

  Logger.log("=================================================");
  Logger.log("BRL Cohort 0 Calendar Successfully Configured!");
  Logger.log("Calendar ID: " + cal.getId());
  Logger.log("=================================================");
}
