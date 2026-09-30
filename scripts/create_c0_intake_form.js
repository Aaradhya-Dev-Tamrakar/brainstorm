/**
 * Brainstorm Research Laboratory (BRL) — Cohort 0 Participant Intake Form Generator
 *
 * FIRST-CONTACT FORM
 * ------------------
 * This form is intentionally lightweight. It is sent with the two short C0
 * briefing documents before formal technical onboarding.
 *
 * To create the form:
 * 1. Open https://script.google.com/
 * 2. Create a new project.
 * 3. Paste this file into Code.gs.
 * 4. Run createBRLCohort0Form().
 * 5. Grant Google Forms permissions.
 * 6. Copy the edit URL and live URL from the execution log.
 */

function createBRLCohort0Form() {
  const formTitle = "Brainstorm Research Laboratory — Cohort 0 Participant Intake";
  const form = FormApp.create(formTitle);

  form.setDescription(
    "This short form helps us understand your background, interests, availability, " +
    "and current setup for Cohort 0 placement.\n\n" +
    "Please read these first:\n" +
    "1. https://github.com/Aaradhya-Dev-Tamrakar/brainstorm/blob/main/research/plans/BRL_C0_OVERVIEW.md\n" +
    "2. https://github.com/Aaradhya-Dev-Tamrakar/brainstorm/blob/main/research/plans/BRL_C0_HOW_IT_WORKS.md\n\n" +
    "This is an intake and placement form, not a technical exam. You do not need prior research experience."
  );

  form.setCollectEmail(true);
  form.setAllowResponseEdits(true);

  // -------------------------------------------------------------
  // SECTION 1: BASIC INFORMATION
  // -------------------------------------------------------------
  form.addSectionHeaderItem()
    .setTitle("1. Basic Information")
    .setHelpText("A few details so we can identify and contact you.");

  form.addTextItem()
    .setTitle("Full Name")
    .setRequired(true);

  form.addTextItem()
    .setTitle("Preferred Name")
    .setHelpText("What should we call you in the cohort?");
  
  form.addTextItem()
    .setTitle("GitHub Username")
    .setHelpText("Enter the username only, without @.")
    .setRequired(true);

  form.addTextItem()
    .setTitle("College / Department / Current Semester")
    .setRequired(true);

  form.addTextItem()
    .setTitle("WhatsApp / Preferred Contact")
    .setRequired(true);

  // -------------------------------------------------------------
  // SECTION 2: CURRENT EXPERIENCE
  // -------------------------------------------------------------
  form.addPageBreakItem()
    .setTitle("2. Current Experience")
    .setHelpText("There is no 'wrong' answer. This helps us start at the right level.");

  addComfortQuestion(
    form,
    "Git / GitHub",
    [
      "Never used",
      "Have seen / used a little",
      "Can do basic tasks",
      "Comfortable using it",
      "Very comfortable"
    ]
  );

  addComfortQuestion(
    form,
    "Python / Programming",
    [
      "Never / almost never",
      "Basic exposure",
      "Can write small programs",
      "Comfortable building small projects",
      "Very comfortable"
    ]
  );

  addComfortQuestion(
    form,
    "Terminal / Command Line",
    [
      "Never used",
      "Basic commands only",
      "Can follow command-line instructions",
      "Comfortable",
      "Very comfortable"
    ]
  );

  addComfortQuestion(
    form,
    "Research / Technical Searching",
    [
      "New to it",
      "Basic",
      "Comfortable finding sources",
      "Comfortable comparing sources",
      "Very comfortable"
    ]
  );

  form.addParagraphTextItem()
    .setTitle("Have you built, investigated, or learned any technical project before?")
    .setHelpText("A short description is enough. Incomplete projects are completely fine.")
    .setRequired(true);

  // -------------------------------------------------------------
  // SECTION 3: INTERESTS
  // -------------------------------------------------------------
  form.addPageBreakItem()
    .setTitle("3. What Interests You?")
    .setHelpText("Select the areas you would most like to explore in C0.");

  form.addCheckboxItem()
    .setTitle("Research Areas You Are Interested In")
    .setChoiceValues([
      "Nepal public-data collection / data mining",
      "AI / Machine Learning",
      "Software engineering / testing",
      "Embedded systems / hardware",
      "Document / language technology",
      "Data analysis / benchmarking",
      "Research experiments / scientific investigation",
      "Systems / infrastructure"
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("What would you most like to learn or become able to do through C0?")
    .setChoiceValues([
      "Learn how to do structured technical research",
      "Learn practical software/data engineering",
      "Work on Nepal-focused data and information",
      "Explore AI/ML through real tasks",
      "Build stronger Git/GitHub and engineering workflow skills",
      "Explore systems / embedded / technical infrastructure",
      "I am still exploring and would like help finding a direction"
    ])
    .setRequired(true);

  // -------------------------------------------------------------
  // SECTION 4: SETUP & AVAILABILITY
  // -------------------------------------------------------------
  form.addPageBreakItem()
    .setTitle("4. Setup & Availability")
    .setHelpText("This helps us avoid assigning work that does not fit your current setup or schedule.");

  form.addMultipleChoiceItem()
    .setTitle("Primary Operating System")
    .setChoiceValues([
      "Windows",
      "Linux",
      "macOS",
      "Windows + WSL",
      "Other"
    ])
    .setRequired(true);

  form.addTextItem()
    .setTitle("Approximate RAM / Laptop or Desktop")
    .setHelpText("Example: 16 GB RAM, Core i5 laptop. Exact specifications are not required.")
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("Realistic Weekly Availability")
    .setChoiceValues([
      "Around 3–4 hours",
      "Around 5–8 hours",
      "Around 9–12 hours",
      "It varies week to week"
    ])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("Known exam / project / travel periods")
    .setHelpText("Mention any upcoming periods when your availability will be low. Write 'None' if there are no known conflicts.")
    .setRequired(true);

  // -------------------------------------------------------------
  // SECTION 5: EXPECTATIONS & INTEREST
  // -------------------------------------------------------------
  form.addPageBreakItem()
    .setTitle("5. Final Check")
    .setHelpText("A few questions about how you would like to participate.");

  form.addMultipleChoiceItem()
    .setTitle("Which statement best describes you right now?")
    .setChoiceValues([
      "I am very new, but I want to learn by doing",
      "I know some basics and want practical experience",
      "I already build projects and want research-oriented challenges",
      "I am mainly interested in exploring and seeing where I fit"
    ])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("Anything else we should know for C0 placement?")
    .setHelpText("Optional — learning goals, constraints, interests, or anything useful.");

  form.addCheckboxItem()
    .setTitle("Participant Understanding")
    .setChoiceValues([
      "I have read the short C0 overview, understand the general model, and would like to be considered for Cohort 0."
    ])
    .setRequired(true);

  Logger.log("=================================================");
  Logger.log("BRL Cohort 0 Participant Intake Form created.");
  Logger.log("Edit Form URL: " + form.getEditUrl());
  Logger.log("Published Live URL: " + form.getPublishedUrl());
  Logger.log("=================================================");
}

function addComfortQuestion(form, title, choices) {
  form.addMultipleChoiceItem()
    .setTitle(title)
    .setChoiceValues(choices)
    .setRequired(true);
}
