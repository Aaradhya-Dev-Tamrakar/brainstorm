@echo off
REM =====================================================================
REM Router CDP Controller - Windows Zero-Friction Runner
REM Usage:
REM   router.bat          (Interactive Console)
REM   router.bat --auto   (1-Click Wi-Fi & DNS Tuning)
REM   router.bat --crawl  (Automated Screenshot Audit)
REM =====================================================================

node "%~dp0cdp_router_manager.js" %*
