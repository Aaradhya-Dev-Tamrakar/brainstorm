# Scaffolding Invariants & Standardized Conventions

## 1. Directory Structure Standards
- Semester root: `[Year-Part]` (e.g. `[IV-I]`, `[IV-II]`).
- Core Subject folders: Named by official course title (e.g., `Telecommunication`, `Engineering Professional Practice`).
- Faculty note subfolders: `Notes by <Initials> Sir` (e.g., `Notes by AKS Sir`, `Notes by PO Sir`).
- Centralized question bank: Dedicated `Past Qns/` at semester root.

## 2. File Naming Patterns
- Past Questions: `<Year>.<Part><program>_<subject>_<type>.pdf`
  - Example: `4.2bei_telecom_old_questions.pdf`, `4.2bei_epp_cases.pdf`.
- Syllabus Extracts: `<Subject>_BEIE_<Year>_<Part>_Syllabus.md`.
- Study Hubs: `StudyHub.md` (must be placed directly inside `<Subject>/` and mirrored to `super-nlm/data/<subject>_guide.md`).

## 3. Mathematical Formula Standards
- Inline math: `$formula$` (wrap literal dollar signs in backticks or escape `\$`).
- Block math:
  $$formula$$
- Every study hub must contain unit mark allocations, core proofs, and an explicit **Exam Traps** section highlighting classic numerical edge cases.
