@echo off
REM ============================================================================
REM build_report.bat - Compiles the formal LaTeX research report inside repo
REM ============================================================================
echo [*] Compiling Brainstorm Research Technical Report (PDF)...
cd "%~dp0report"
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
if exist main.pdf (
    echo [x] SUCCESS: Compiled report/main.pdf successfully!
) else (
    echo [!] ERROR: Compilation failed. Check report/main.log for details.
)
cd "%~dp0"
