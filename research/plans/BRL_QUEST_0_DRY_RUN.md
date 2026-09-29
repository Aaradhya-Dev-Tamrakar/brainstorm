# Quest C0-00: The Onboarding Litmus Test (Quest 0)

**ID:** `QUEST-C0-00`  
**Rank Requirement:** Unranked $\rightarrow$ Rank E (*Research Scout*)  
**Estimated Time:** 30–45 minutes  
**Target Subsystem:** Contributor Registry & Environment Tooling  
**Prerequisites:** Git installed, Python 3.10+ installed, GitHub account  

---

## 1. Objective

Complete the end-to-end laboratory onboarding loop. This quest verifies your local development environment, Git credential configuration, terminal execution, and comprehension of the repository's deterministic audit gate (`.\audit.bat`) before undertaking substantive research quests.

---

## 2. Step-by-Step Execution Protocol

### Step 1: Clone the Repository
Clone the central repository and navigate into the root directory:
```bash
git clone https://github.com/Aaradhya-Dev-Tamrakar/brainstorm.git
cd brainstorm
```

### Step 2: Configure Git Identity
Ensure your local Git commits reflect your real name and GitHub-linked email address:
```bash
git config user.name "Your Full Name"
git config user.email "your_email@example.com"
```

### Step 3: Create an Isolated Contributor Branch
Do **not** make edits directly on `main`. Create an isolated feature branch following the strict naming convention:
```bash
# Branch format: c0/<github_username>/quest-0
# Example:
git checkout -b c0/roshan-kc/quest-0
```

### Step 4: Create Your Fellow Profile
Copy the fellow profile template and fill in your details:
```bash
# Copy the template to your username markdown file
cp research/fellows/TEMPLATE.md research/fellows/<your_github_username>.md
```
Open `research/fellows/<your_github_username>.md` in your editor and fill out:
- Full Name
- College / Faculty / Current Semester
- GitHub Username
- Primary Technical Competencies
- Local Hardware Setup (OS, RAM, GPU)
- Top 2 Quest Preferences from [`PLAN-BRL-001`](PLAN-BRL-001_BRAINSTORM_RESEARCH_LAB_CHARTER.md)

### Step 5: Execute the Zero-Discrepancy Audit Gate
Run the repository verification suite to confirm that your profile addition introduces zero syntax errors, broken links, or schema regressions:
```bash
# On Windows (PowerShell or Command Prompt):
.\audit.bat

# On Linux / macOS / WSL:
./audit.sh   # or: python sim/reconciliation_engine.py --audit-only
```
**Acceptance Condition:** The terminal must output:
`[+] PASS: Layer 1 (Structural Consistency) is 100% verified (0 discrepancies).`

### Step 6: Commit and Push
Stage and commit your changes using a clean conventional commit message:
```bash
git add research/fellows/<your_github_username>.md
git commit -m "docs(fellows): add contributor profile for <your_github_username> (Quest 0)"
git push origin c0/<your_github_username>/quest-0
```

### Step 7: Open a Pull Request
1. Open the GitHub repository in your browser.
2. Click **Compare & pull request** for your branch.
3. Fill out the Pull Request template:
   - Mark the checklist items.
   - Attach a snippet or confirmation of the passing `.\audit.bat` run.
4. Submit the PR for review by the Laboratory Director (`AaradhyaDT`).

---

## 3. Evaluation & Rank Advancement

Upon PR merge:
- You are formally recognized as an active **Rank E Research Scout** in the Brainstorm Research Laboratory.
- Your official Quest 1 assignment (`C0-01`, `C0-02`, `C0-03`, or `C0-04`) will be unlocked and assigned in GitHub Issues.
