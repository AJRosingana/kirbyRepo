# KirbyRepo — Minimalist Demo & Modular Reciprocal Architecture

This document defines the requirements, minimalist demo blueprint, and modular reciprocal architecture for evolving **KirbyRepo** from validated prototypes into a swappable, agentic multi-OS companion framework.

---

## 1. Validated Core Primitives (Baseline)
- **Desktop Toy (`kirby_magician_tac`):** Verified cursor-swap illusion where Magician Kirby swaps the cursor on-screen and Tac runs in, grabs the fake cursor, and bolts off-screen.
- **Android UX Overlay (`KirbyNativeOverlayService`):** Verified floating Android overlay with roaming, dual chat bubbles, and Quick Settings **Scarce Mode** toggle (`KirbyScarceTileService`).

---

## 2. Rudimentary Fundamentals — Minimum Requirements Matrix

| Layer | Android OS | Linux (Desktop / CLI) | Windows 11 | Web (Browser Demo) |
| :--- | :--- | :--- | :--- | :--- |
| **Overlay / Surface** | `SYSTEM_ALERT_WINDOW` + `WindowManager` (`TYPE_APPLICATION_OVERLAY`) | X11/Wayland transparent window or terminal ANSI/curses | WPF transparent topmost window (`AllowsTransparency=True`) | Single-file HTML5 `<canvas>` / CSS overlay |
| **Foreground / Persistence** | `FOREGROUND_SERVICE` (`specialUse`) + Quick Settings `TileService` | Background daemon / `tmux` / `systemd --user` | PowerShell/`.bat` launcher + Core 0 affinity mask (`0xFE`) | Browser tab / PWA |
| **Input / Cursor Toys** | Touch/drag listeners on overlay views *(for system-wide UI actions: AccessibilityService)* | Python stdlib (`tkinter` / `curses`) or `xdotool` / `evdev` | Win32 `User32.dll` cursor/window hooks via PowerShell P/Invoke | Pointer events (`pointermove`, `pointerdown`) |
| **Reciprocal Event Bus** | Local HTTP/WebSocket (`KirbyVisitorAccessPointService`, port `8088`) | Local Unix socket / stdio JSON-lines / HTTP | Local HTTP/WebSocket to Linux/Android hub | WebSocket / `BroadcastChannel` / `postMessage` |

---

## 3. Track A — Minimalist Demo (Near-Zero Dependencies)
**Objective:** A stripped-down, immediately runnable demo derived from the validated primitives, with **as few dependencies as possible**, designed for external feedback.

### Demo Scope
1. **Zero-Dependency Web/HTML Toy (1 file):** Recreates the **Magician Kirby & Tac cursor-heist** and roaming buddy in a single standalone `.html` file (vanilla JS + Canvas, no `node_modules` required).
2. **Minimal Python CLI Demo (stdlib only):** Single-script terminal buddy (`python3` stdlib only) demonstrating the reciprocal command/event loop.
3. **Minimal Android Overlay APK:** Lean `KirbyNativeOverlayService` + `MainActivity` toggle + `KirbyScarceTileService` (no heavy web/game dependencies).

### Architectural Extension Pointers (Where Higher Functions Plug In)
Each demo component exposes explicit, documented hook points showing how to expand:
- **`[EXT:AGENT_BRAIN]`** — Plug in an LLM / AGY CLI agent over local JSON-RPC/HTTP to turn scripted chirps into context-aware actions.
- **`[EXT:UI_AUTOMATION]`** — Expand from passive overlay to active UX/UI interaction:
  - *Android:* Requires `AccessibilityService` (or `adb` / `uiautomator`) to inspect/tap UI nodes.
  - *Linux/Win11:* Requires AT-SPI / X11 / Win32 UI Automation hooks.
- **`[EXT:PHYSICS_TOYS]`** — Plug in interactive overlay entities (e.g., **Kirby Beach Ball** 2D bounce/chase physics).
- **`[EXT:OS_BUBBLE]`** — Plug in Android `Notification.BubbleMetadata` for an expandable MindMesh chat/control sheet.
- **`[EXT:ASSET_PACK]`** — Swap sprites, animations, palettes, and layouts via a JSON manifest without touching engine code.

---

## 4. Track B — Modular Reciprocal Architecture (Full Version)
Every module is swappable and communicates **bidirectionally (to/from)** with its neighbors via a shared JSON event contract:

```text
+-------------------+       +-------------------+       +-------------------+
|  Asset / Skin     | <---> |  Behavior / Toy   | <---> |  Agentic Backend  |
|  Pack Module      |       |  Module           |       |  (Python / Linux) |
| (Sprites, Anims,  |       | (Magician/Tac,    |       | (AGY CLI, Tools,  |
|  Layouts, Shaders)|       |  Beach Ball, HUD) |       |  Memory, Policy)  |
+-------------------+       +-------------------+       +-------------------+
          ^                           ^                           ^
          |                           |                           |
          v                           v                           v
+---------------------------------------------------------------------------+
|               OS Surface Adapter (Android / Linux / Win11 / Web)          |
|         (Renders visuals, captures gestures/cursor, enforces Scarce Mode) |
+---------------------------------------------------------------------------+
```

### Reciprocal Contract (To / From)
- **Surface → Behavior/Backend:** `gesture`, `cursor_pos`, `active_app`, `scarce_mode_changed`, `toy_collision`.
- **Backend/Behavior → Surface:** `move_to`, `play_anim`, `swap_cursor`, `spawn_bubble`, `set_shader`, `set_scarce_mode`.
- **Asset Pack ↔ Surface/Behavior:** Declares sprite sheets, frame timings, hitboxes, and layout anchors so any character or theme can drop in cleanly.
