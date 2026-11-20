# KirbyRepo — Multi-OS Kirby & Macro Portal Engine

A multi-platform suite combining the **Macro Portal Engine** web app with native **Android HUD**, **Linux CLI**, and **Windows 11** Kirby companions.

---

## Repository Layout

| Directory | Target | Stack & Highlights |
| :--- | :--- | :--- |
| [`src/`](./src) & [`server.ts`](./server.ts) | **Macro Portal Engine (Web)** | React 19, Vite 6, TypeScript 5.8, Tailwind CSS 4, Express, `@google/genai` |
| [`android/android_hud_app/`](./android/android_hud_app) | **Android HUD APK** | Kotlin, ViewBinding, API 35, Floating Overlay Service, Visitor AP (port `8088`), Quick Settings **Scarce Mode** tile, AGSL shaders |
| [`linux/`](./linux) | **Linux CLI & Scripts** | Bash entrypoints (`kirby`, `launch_kirby.sh`) + 25 Python 3 modules (`linux/scripts/`) |
| [`win11/`](./win11) | **Windows 11 Companion** | PowerShell WPF overlay, Edge companion, Core 0 affinity isolation (`0xFE`) |

---

## Quick Start

### Web App (Macro Portal Engine)
```bash
bun install
bun run dev      # Dev server (tsx server.ts)
bun run lint     # TypeScript check (tsc --noEmit)
bun run build    # Production Vite + esbuild bundle
```

### Android HUD APK
```bash
cd android/android_hud_app
gradle assembleDebug
# Output: app/build/outputs/apk/debug/app-debug.apk
```
*(Also built automatically on push via [`.github/workflows/android-debug-apk.yml`](./.github/workflows/android-debug-apk.yml).)*

### Linux CLI
```bash
./linux/launch_kirby.sh
```
See [`linux/KIRBY_STARTER_GUIDE.md`](./linux/KIRBY_STARTER_GUIDE.md) for full usage.

### Windows 11 Companion
See [`win11/README.md`](./win11/README.md) for 1-click safe-mode launchers.

---

## Roadmap / TODO
- [ ] **Interactive Kirby Beach Ball Overlay:** Physics-driven floating beach ball in `KirbyNativeOverlayService` that Kirby can chase, bonk, and act upon.
- [ ] **Android OS Bubble (`BubbleMetadata`):** Native Android bubble integration for expanding the MindMesh portal/chat sheet.
- [ ] **Windows 11 Polish:** Further testing & polish for `win11/` and `kirby_magician_tac` modules.
