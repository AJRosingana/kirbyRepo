@echo off
title 🌸 Kirby Win11 Desktop Companion Launcher (Affinity Shielded) 🌸
color 0D

echo ==============================================================================
echo   ⭐ (•_•)و 🌸 OPERATION STARFALL POYO: WIN11 DESKTOP COMPANION 🌸 (•_•)੭ ⭐
echo   Host: ajr-win11-lappy • Mesh Node-A: 100.121.245.47:8088
echo   CPU Shield: Core 0 DISABLED (Affinity 0xFE) • Priority: BelowNormal
echo ==============================================================================
echo.
echo Choose your Kirby Companion launch mode:
echo   [1] Native Windows 11 WPF Overlay (Safe Affinity 0xFE, BelowNormal Priority)
echo   [2] High-DPI Edge App Companion (Safe Affinity 0xFE, GPU-Accelerated)
echo   [3] Dual Mode (Native Overlay + Edge Toolbox, Core 0 Shielded)
echo   [4] Open Local HTML Companion in Default Browser
echo   [5] ⚡ Ultra-Safe Eco Mode (30 FPS Cap, Core 0 Isolated, Clean Restart)
echo   [6] ⚔️ Cloned Kung Fu Combat Overlay (Dual Fighters & Multi-Wrappers)
echo   [7] 🧹 Clean Kill (Terminate all stuck/lagging Kirby instances)
echo.
set /p CHOICE="Enter choice (1-7, default 1): "

if "%CHOICE%"=="" set CHOICE=1

if "%CHOICE%"=="1" (
    echo.
    echo [*] Launching Native Windows 11 WPF Companion (Core 0 Shielded)...
    start "" /belownormal /affinity FE powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0kirby_win11_invasion.ps1"
    goto end
)

if "%CHOICE%"=="2" (
    echo.
    echo [*] Launching Edge App Companion (Core 0 Shielded)...
    start "" /belownormal /affinity FE msedge.exe --app=http://100.121.245.47:8088/win11 --window-size=560,780 --enable-gpu-rasterization --enable-zero-copy
    goto end
)

if "%CHOICE%"=="3" (
    echo.
    echo [*] Launching Dual Engine Companion (Core 0 Shielded)...
    start "" /belownormal /affinity FE powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0kirby_win11_invasion.ps1"
    timeout /t 2 /nobreak >nul
    start "" /belownormal /affinity FE msedge.exe --app=http://100.121.245.47:8088/win11 --window-size=560,780 --enable-gpu-rasterization --enable-zero-copy
    goto end
)

if "%CHOICE%"=="4" (
    echo.
    echo [*] Opening Local HTML Companion...
    start "" "%~dp0kirby_win11_companion.html"
    goto end
)

if "%CHOICE%"=="5" (
    echo.
    echo [*] Terminating any ghost instances & launching Ultra-Safe Eco Mode...
    powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-Process -Name powershell, pwsh -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like '*Kirby*' -or $_.CommandLine -like '*kirby_win11_invasion*' } | Stop-Process -Force -ErrorAction SilentlyContinue"
    timeout /t 1 /nobreak >nul
    start "" /belownormal /affinity FE powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0kirby_win11_invasion.ps1" -SafeMode -KillExisting
    goto end
)

if "%CHOICE%"=="6" (
    echo.
    echo [*] Launching Cloned Kung Fu Combat Overlay (Dual Fighters & Multi-Wrappers)...
    start "" /belownormal /affinity FE msedge.exe --app="%~dp0kirby_cloned_combat_overlay.html" --window-size=1020,740 --enable-gpu-rasterization --enable-zero-copy
    goto end
)

if "%CHOICE%"=="7" (
    echo.
    echo [*] Terminating all Kirby companion processes...
    powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-Process -Name powershell, pwsh -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like '*Kirby*' -or $_.CommandLine -like '*kirby_win11_invasion*' } | Stop-Process -Force -ErrorAction SilentlyContinue; Get-Process -Name msedge -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*:8088/win11*' -or $_.CommandLine -like '*combat_overlay*' } | Stop-Process -Force -ErrorAction SilentlyContinue"
    echo [✔] Cleaned up all Kirby instances.
    pause
    exit /b 0
)

:end
echo.
echo [✔] Kirby is arriving with Core 0 Shielding! Poyo! 🌸
timeout /t 3 >nul
exit /b 0
