# 🌸 Operation Starfall Poyo: Windows 11 Kirby Desktop Companion
**Target: `ajr-win11-lappy` • Tailscale: `100.87.84.94` • Home Node: Pixel 9 Pro XL (`100.121.245.47`)**

```
       .---.          ⭐
      /     \       / | \
     | () () |   -- * - * --  ✨ Poyo! Kirby on Win11 (Safe Mode & Core 0 Isolated)! ✨
      \  =  /       \ | /
     .-'---'-.        ⭐
    /         \
```

---

## ⚡ Zero-UX-Lag Architecture & Core 0 Isolation Shield

On Windows 11, the **Desktop Window Manager (`dwm.exe`)**, shell input queue, and kernel interrupts heavily rely on **CPU Core 0**. When background worker apps or WPF overlays run on Core 0, the desktop UX can experience hitching, cursor micro-stutter, and frame drops.

To guarantee **100% butter-smooth Windows 11 UI/UX**:
1. **Core 0 Disabled (Affinity 0xFE / Non-Zero Mask)**: Both the PowerShell engine and Edge app are explicitly masked off from Core 0. They execute strictly on Cores 1+.
2. **Process Priority (`BelowNormal`)**: Ensures Windows shell and foreground apps always receive priority input scheduling.
3. **Single-Instance Mutex Protection (`Global\KirbyWin11Companion_SingleInstance_Mutex`)**: Prevents duplicate ghost instances even when scripts are executed repeatedly.
4. **Idle-Sleep Particle Engine**: WebGL/Canvas rendering completely ceases (`0.0% CPU`) when no stardust particles are in flight.
5. **rAF-Throttled Mousemove**: Eye tracking and DOM writes are capped to display refresh frames rather than unthrottled mouse events.

---

## 🚀 1-Click Launch Options on Windows 11

### 1. ⚡ 1-Click Instant Safe Mode (Recommended)
Double-click:
[`launch_kirby_win11_safe.bat`](./launch_kirby_win11_safe.bat)
- Terminates any previous ghost/lagging instances.
- Automatically disables CPU Core 0 (`/affinity FE`).
- Sets priority to `BelowNormal`.
- Caps WPF animation timeline to 30 FPS.
- Zero prompts, instant safe launch!

### 2. 🎛️ Interactive Launcher
Double-click:
[`launch_kirby_win11.bat`](./launch_kirby_win11.bat)
Choose:
- `[1]` Native Windows 11 WPF Overlay (Safe Affinity `0xFE`).
- `[2]` High-DPI Edge App Companion (Safe Affinity `0xFE`, GPU-Accelerated).
- `[3]` Dual Mode (Native Overlay + Edge Toolbox).
- `[4]` Open Local HTML Companion in Default Browser.
- `[5]` ⚡ Ultra-Safe Eco Mode (30 FPS Cap, Core 0 Isolated).
- `[6]` 🧹 Clean Kill (Terminate all Kirby instances).

### 3. 🌐 Edge App Companion (Frameless Window)
Double-click:
[`launch_edge_companion.bat`](./launch_edge_companion.bat)
- Launched with `/belownormal /affinity FE` and GPU rasterization flags.
- Direct URL: `http://100.121.245.47:8088/win11`.

### 4. 🛡️ CPU Affinity & Core 0 Shield Audit Tool
Run in PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File .\apply_win11_safe_affinity.ps1
```
Or run continuous watcher:
```powershell
powershell -ExecutionPolicy Bypass -File .\apply_win11_safe_affinity.ps1 -Watch -IntervalSec 5
```
Automatically audits all mesh/companion processes and strips Bit 0 (Core 0).

### 5. 🧹 Emergency Stop / Cleanup
Double-click:
[`kill_kirby_win11.bat`](./kill_kirby_win11.bat)
Instantly terminates all Kirby PowerShell and Edge companion processes.

---

## 🔒 The "Just Kirby Though" Guarantee
In accordance with mission directives, only Kirby participates in this desktop companion. No Noid gremlins, no annoying pizza snatches, no clutter. Just pure, cheerful, loyal Dream Land companionship!
