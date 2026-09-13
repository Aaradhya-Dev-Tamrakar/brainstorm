@echo off
REM ============================================================================
REM archive.bat - Verbatim transcript export shortcut per INV-EPI-001
REM Usage:
REM   archive.bat               (automatic significance detection)
REM   archive.bat MY-CODENAME   (archive with specific codename)
REM ============================================================================
if "%~1"=="" (
    python "%~dp0sim\transcript_archiver.py" --auto
) else (
    python "%~dp0sim\transcript_archiver.py" --codename "%~1"
)
