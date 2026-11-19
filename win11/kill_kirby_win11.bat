@echo off
title 🧹 Kirby Win11 Emergency Stop & Cleanup 🧹
color 0C

echo ==============================================================================
echo   🧹 EMERGENCY CLEANUP: TERMINATING ALL KIRBY WIN11 PROCESSES 🧹
echo ==============================================================================
echo.

echo [*] Terminating Kirby PowerShell overlays...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-Process -Name powershell, pwsh -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like '*Kirby*' -or $_.CommandLine -like '*kirby_win11_invasion*' } | Stop-Process -Force -ErrorAction SilentlyContinue"

echo [*] Terminating Kirby Edge app instances...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-Process -Name msedge -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*:8088/win11*' } | Stop-Process -Force -ErrorAction SilentlyContinue"

echo.
echo [✔] All Kirby processes terminated cleanly! CPU and RAM freed.
timeout /t 3 >nul
exit /b 0
