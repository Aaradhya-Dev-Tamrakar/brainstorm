#!/usr/bin/env python3
"""
scaffold_thesis.py — Multi-Template LaTeX Thesis, Capstone & Beamer Scaffolder
Part of latex-thesis-architect skill.

Supports:
1. 'engineering-report' (alias: 'report') : Academic Engineering Report (engineering-report.cls)
2. 'beamer-presentation' (alias: 'beamer'): Widescreen 16:9 Beamer Deck (beamer-presentation.cls)
3. 'capstone-report' (alias: 'capstone')  : Capstone / Monograph Report (at_fuse_aif.cls)
4. 'full-pack' (alias: 'all')             : Scaffolds both report/ and presentation/ side-by-side
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

TEMPLATES_ROOT = Path(__file__).resolve().parent.parent / "assets" / "templates"

VARS_TEMPLATE = """% =========================================
%               Custom Variables
% =========================================
\\newcommand\\cUniversity{{{university}}}
\\newcommand\\cDepartment{{{department}}}
\\newcommand\\cCampus{{{campus}}}
\\newcommand\\cDocumentType{{{doc_type}}}
\\newcommand\\cTitle{{{title}}}
\\newcommand\\cTitleShort{{{short_title}}}

% =========================================
%          Author Information
% =========================================
\\renewcommand\\cSubmittedI{{{author1}}}
\\renewcommand\\cSubmittedII{{{author2}}}
\\renewcommand\\cSubmittedIII{{{author3}}}
\\renewcommand\\cSubmittedIV{{{author4}}}

\\renewcommand\\cSubmittedIRoll{{{roll1}}}
\\renewcommand\\cSubmittedIIRoll{{{roll2}}}
\\renewcommand\\cSubmittedIIIRoll{{{roll3}}}
\\renewcommand\\cSubmittedIVRoll{{{roll4}}}

% =========================================
%          Faculty Information
% =========================================
\\newcommand\\cSupervisor{{{supervisor}}}
\\newcommand\\cSupervisorTitle{{{supervisor_title}}}
\\newcommand\\cSupervisorDept{{{supervisor_dept}}}
\\newcommand\\cSupervisorAddress{{{supervisor_address}}}

% Project Coordinator Info
\\newcommand\\cProjectCoordinator{{{coordinator}}}
\\newcommand\\cProjectCoordinatorTitle{{{coordinator_title}}}
\\newcommand\\cProjectCoordinatorDept{{{coordinator_dept}}}
\\newcommand\\cProjectCoordinatorAddress{{{coordinator_address}}}

% HOD Info
\\newcommand\\cHOD{{{hod}}}
\\newcommand\\cHODTitle{{{hod_title}}}
\\newcommand\\cHODDept{{{hod_dept}}}
\\newcommand\\cHODAddress{{{hod_address}}}

% External Examiner Info
\\newcommand\\cExternalExaminer{{{examiner}}}
\\newcommand\\cExternalExaminerTitle{{{examiner_title}}}
\\newcommand\\cExternalExaminerDept{{{examiner_dept}}}
\\newcommand\\cExternalExaminerAddress{{{examiner_address}}}

% Date Formats
\\newcommand\\cDate{{{date_month_year}}}
\\newcommand\\cDateFull{{{date_full}}}
"""

LATEX_GITIGNORE = """# LaTeX compilation output artifacts
*.aux
*.bbl
*.bcf
*.blg
*.dvi
*.fdb_latexmk
*.fls
*.glg
*.glo
*.gls
*.idx
*.ilg
*.ind
*.ist
*.log
*.nav
*.out
*.snm
*.synctex(busy)
*.synctex.gz
*.toc
*.lot
*.lof
*.vrb
*.run.xml
*.acn
*.acr
*.alg
*.slo
*.sls
*.slg
*.sta
indent.log
"""


def scaffold_report(template_dir: Path, target_dir: Path, args: argparse.Namespace) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)

    for item in template_dir.iterdir():
        dest = target_dir / item.name
        if item.name == "vars.tex":
            continue
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    vars_content = VARS_TEMPLATE.format(
        university=args.university,
        department=args.dept,
        campus=args.campus,
        doc_type=args.doc_type,
        title=args.title,
        short_title=args.short_title or args.title[:50],
        author1=args.author1,
        author2=args.author2 or "",
        author3=args.author3 or "",
        author4=args.author4 or "",
        roll1=args.roll1 or "",
        roll2=args.roll2 or "",
        roll3=args.roll3 or "",
        roll4=args.roll4 or "",
        supervisor=args.supervisor or "Supervisor Name",
        supervisor_title=args.supervisor_title or "Supervisor Title",
        supervisor_dept=args.supervisor_dept or args.dept,
        supervisor_address=args.supervisor_address or args.campus,
        coordinator=args.coordinator or "Project Coordinator",
        coordinator_title=args.coordinator_title or "Project Coordinator",
        coordinator_dept=args.coordinator_dept or args.dept,
        coordinator_address=args.coordinator_address or args.campus,
        hod=args.hod or "Head of Department",
        hod_title=args.hod_title or "Head of Department",
        hod_dept=args.hod_dept or "Department of Engineering",
        hod_address=args.hod_address or args.campus,
        examiner=args.examiner or "External Examiner",
        examiner_title=args.examiner_title or "External Examiner",
        examiner_dept=args.examiner_dept or "External Institution",
        examiner_address=args.examiner_address or "City, Country",
        date_month_year=args.date_month or "Month Year",
        date_full=args.date_full or "Month DD, YYYY",
    )
    (target_dir / "vars.tex").write_text(vars_content, encoding="utf-8")

    gitignore_path = target_dir / ".gitignore"
    if not gitignore_path.exists():
        gitignore_path.write_text(LATEX_GITIGNORE, encoding="utf-8")


def scaffold_beamer(template_dir: Path, target_dir: Path, args: argparse.Namespace) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)

    for item in template_dir.iterdir():
        dest = target_dir / item.name
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    gitignore_path = target_dir / ".gitignore"
    if not gitignore_path.exists():
        gitignore_path.write_text(LATEX_GITIGNORE, encoding="utf-8")


def resolve_template_name(raw_name: str) -> str:
    mapping = {
        "report": "engineering-report",
        "engineering-report": "engineering-report",
        "tcioe-report": "engineering-report",
        "tcioe": "engineering-report",
        "beamer": "beamer-presentation",
        "beamer-presentation": "beamer-presentation",
        "tcioe-beamer": "beamer-presentation",
        "capstone": "capstone-report",
        "capstone-report": "capstone-report",
        "fuse-aif": "capstone-report",
        "full-pack": "full-pack",
        "pack": "full-pack",
        "all": "full-pack",
    }
    return mapping.get(raw_name.lower(), "engineering-report")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold LaTeX Thesis / Capstone / Beamer Workspace")
    parser.add_argument("target_dir", type=Path, help="Target directory for the project")
    parser.add_argument(
        "--template",
        default="engineering-report",
        help="Template to scaffold: engineering-report (default/report), beamer-presentation (beamer), capstone-report (capstone), or full-pack",
    )
    parser.add_argument("--title", required=True, help="Full project/thesis title")
    parser.add_argument("--short-title", help="Abbreviated title")
    parser.add_argument("--university", default="University Name", help="University name")
    parser.add_argument("--dept", default="Department of Engineering", help="Department")
    parser.add_argument("--campus", default="Campus / Institution", help="Campus / Location")
    parser.add_argument("--doc-type", default="A MAJOR PROJECT REPORT", help="Document type")
    parser.add_argument("--author1", required=True, help="First author")
    parser.add_argument("--author2", help="Second author")
    parser.add_argument("--author3", help="Third author")
    parser.add_argument("--author4", help="Fourth author")
    parser.add_argument("--roll1", help="Roll number 1 (e.g. ROLL-001)")
    parser.add_argument("--roll2", help="Roll number 2")
    parser.add_argument("--roll3", help="Roll number 3")
    parser.add_argument("--roll4", help="Roll number 4")
    parser.add_argument("--supervisor", help="Supervisor name")
    parser.add_argument("--supervisor-title", help="Supervisor title")
    parser.add_argument("--supervisor-dept", help="Supervisor dept")
    parser.add_argument("--supervisor-address", help="Supervisor address")
    parser.add_argument("--coordinator", help="Project coordinator")
    parser.add_argument("--coordinator-title", help="Project coordinator title")
    parser.add_argument("--coordinator-dept", help="Project coordinator dept")
    parser.add_argument("--coordinator-address", help="Project coordinator address")
    parser.add_argument("--hod", help="Head of Department")
    parser.add_argument("--hod-title", help="HOD title")
    parser.add_argument("--hod-dept", help="HOD dept")
    parser.add_argument("--hod-address", help="HOD address")
    parser.add_argument("--examiner", help="External examiner")
    parser.add_argument("--examiner-title", help="External examiner title")
    parser.add_argument("--examiner-dept", help="External examiner dept")
    parser.add_argument("--examiner-address", help="External examiner address")
    parser.add_argument("--date-month", default="Month Year", help="Date in 'Month Year' format")
    parser.add_argument("--date-full", default="Month DD, YYYY", help="Full date format")

    args = parser.parse_args()
    tmpl = resolve_template_name(args.template)

    if tmpl == "full-pack":
        report_dir = args.target_dir / "report"
        pres_dir = args.target_dir / "presentation"
        print(f"[*] Scaffolding Full Pack (Report + Beamer) in {args.target_dir}...")
        scaffold_report(TEMPLATES_ROOT / "engineering-report", report_dir, args)
        scaffold_beamer(TEMPLATES_ROOT / "beamer-presentation", pres_dir, args)
        print(f"[SUCCESS] Scaffolding complete:")
        print(f"  Report:       {report_dir}")
        print(f"  Presentation: {pres_dir}")
    elif tmpl == "engineering-report":
        print(f"[*] Scaffolding engineering report template in {args.target_dir}...")
        scaffold_report(TEMPLATES_ROOT / "engineering-report", args.target_dir, args)
        print(f"[SUCCESS] Scaffolding complete at {args.target_dir}")
    elif tmpl == "capstone-report":
        print(f"[*] Scaffolding capstone report template in {args.target_dir}...")
        scaffold_report(TEMPLATES_ROOT / "fuse-aif", args.target_dir, args)
        print(f"[SUCCESS] Scaffolding complete at {args.target_dir}")
    elif tmpl == "beamer-presentation":
        print(f"[*] Scaffolding Beamer presentation in {args.target_dir}...")
        scaffold_beamer(TEMPLATES_ROOT / "beamer-presentation", args.target_dir, args)
        print(f"[SUCCESS] Scaffolding complete at {args.target_dir}")


if __name__ == "__main__":
    main()
