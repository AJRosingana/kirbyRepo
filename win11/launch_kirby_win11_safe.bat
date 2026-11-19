@echo off
title 🌸 Kirby Win11 1-Click Safe Mode Launcher 🌸
color 0A

echo ==============================================================================
echo   ⚡ 🌸 KIRBY WIN11 1-CLICK SAFE MODE LAUNCHER (CORE 0 ISOLATED) 🌸 ⚡
echo   Target: ajr-win11-lappy • CPU Shield: Core 0 DISABLED (Mask 0xFE)
echo   Priority: BelowNormal • 30 FPS Cap • Mutex Deduplicated
echo ==============================================================================
echo.

echo [*] Terminating any existing ghost/lagging companion instances...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-Process -Name powershell, pwsh -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like '*Kirby*' -or $_.CommandLine -like '*kirby_win11_invasion*' } | Stop-Process -Force -ErrorAction SilentlyContinue"

timeout /t 1 /nobreak >nul

echo [*] Launching Native Kirby Companion in Safe Mode (Core 0 Excluded)...
start "" /belownormal /affinity FE powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0kirby_win11_invasion.ps1" -SafeMode -KillExisting

echo.
echo [✔] Kirby is safely soaring in on his Warp Star! Zero UI lag guaranteed! Poyo! 🌸
timeout /t 3 >nul
exit /b 0
