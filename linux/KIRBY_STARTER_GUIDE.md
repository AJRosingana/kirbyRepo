# 🌸 Kirby uX fX Ecosystem & Dev Compendium Guide
**Pixel 9 Pro XL • Android 16 • MindMesh Floating Overlay, Multi-Squad Roster, WebGL 3D, Audio-Haptics & Games**  
*Location: [`/home/droid/KIRBY_STARTER_GUIDE.md`](file:///home/droid/KIRBY_STARTER_GUIDE.md) • Unified CLI: [`kirby`](file:///home/droid/.local/bin/kirby) | [`launch_kirby.sh`](file:///home/droid/launch_kirby.sh)*

---

## 1. 🚀 Unified CLI Command Reference

The global `kirby` command provides end-to-end orchestration of all Kirby systems across Linux Terminal VM, Termux, and Android OS:

### A. Core HUD & Phone Overlay
```bash
kirby start               # Launch Kirby Floating Overlay HUD on Pixel 9 Pro XL screen
kirby stop                # Stop and dismiss Kirby to Dream Land
kirby restart             # Clean restart of Kirby Overlay
kirby status              # Audit all Kirby services, ADB bridge, and mesh ports
kirby snap                # Capture instant screenshot of screen with Kirby visible
kirby visitor [act]       # Query/trigger on-device Visitor Service (status|enter|react)
```

### B. Multi-Kirby Squad & Party Deck
```bash
kirby squad [status]      # View 4-member active party and complete 10-Kirby roster
kirby party <k1> <k2>...  # Configure 4-member active party (e.g. kirby_prime noid_kirby)
kirby banter              # Trigger live conversational banter between Kirbies
kirby raid [dungeon]      # Dispatch 4-Kirby party on co-op dungeon raid for Star Coins
```

### C. Reflex Showdowns & Minigames
```bash
kirby samurai             # Play legendary Samurai Kirby Quick Draw reflex duel
kirby quickdraw [--auto]  # Quick Draw duel with microsecond reaction timing
kirby play | game         # Launch terminal arcade game: Star Catcher ( ^-^ )
kirby auto                # Run Star Catcher in AI auto-pilot mode
kirby typey | chaotix     # Ephemeral mechanical typing & kinetic physics arena
kirby tappa [live|adb]    # ProjectM Visualizer tap dancer & physical screen co-tapper
```

### D. Magician Sleight & Cosmic Oracle
```bash
kirby magician [act]      # Run 4-Act Magician Kirby & Tac sleight-of-hand screenplay
kirby tarot               # Draw a Tarot Card from the Magician Top Hat
kirby oracle [query]      # Consult the Oracle of Poyo for cosmic development advice
kirby 20q                 # Play Kirby's Reverse 20Q Intent Genie
kirby sprites [name]      # ANSI multi-frame ASCII sprite animator (warp, bounce, etc.)
kirby studio [cmd]        # Procedural ASCII art painter & gallery (generate|gallery)
```

### E. Needs, Sanctuary & Holistic Wellbeing
```bash
kirby needs [status]      # Holistic 8 Core Needs & 10 Squad Desires Matrix
kirby needs auto          # Autonomous Caregiver: bring all 8 needs & squad desires to 100%
kirby nap | sleep         # Starlight Dream Nap on a fluffy Dream Cloud (100% Energy)
kirby wake                # Gently awaken Kirby with morning starlight
kirby bath | spa | wash   # Fountain of Dreams bubble spa bath (100% Hygiene)
kirby hug | cuddle        # Tender loving hug & head pats (100% Affection & Bond XP)
kirby fengshui | comfort  # Harmonize room Spatial Feng Shui & cozy Qi (100% Sanctuary)
kirby cool | chill        # Freeze Kirby Glacial Chill to cool CPU thermals to 34°C
kirby fulfill <need>      # Fulfill specific need (satiety, rest, bath, hug, etc.)
kirby sanctuary           # Open Kirby Needs Sanctuary Web Portal (:8088/needs)
kirby caretaker [status]  # Bandana Dee & Chef Kawasaki Caretaker Duo HQ
kirby caretaker round     # Proactive squad wellness round
kirby caretaker mutual    # Mutual caregiving ritual ("They take care of one another")
kirby buddy               # Alias for mutual care ritual
kirby tuck [target]       # Bandana Dee tucks Kirby into bed with warm fleece blanket
kirby cook [dish]         # Chef Kawasaki cooks fresh vitality ramen or stew
```

### F. Care, Expeditions & Combat
```bash
kirby pet [status]        # Tamagotchi care, hunger, energy & bond levels
kirby feed <item>         # Feed Maxi Tomato (🍅), Strawberry Shortcake, or Star Candy
kirby mood                # Inspect Kirby's live mood and facial expression
kirby expedition [zone]   # Embark on Dream Land expeditions & quests (Green Greens, Halberd, etc.)
kirby boss [name]         # Boss Colosseum duel (Whispy Woods, Dedede, Meta Knight, Marx)
kirby clean [--dry-run]   # Hypernova Inhale deep clean of stale cache & screen snaps
```

### G. Noid Gremlin Chaos & Mischief
```bash
kirby noid                # Noid Gremlin status, chaos meter & prank inventory
kirby prank [target]      # Deploy a hilarious gremlin prank across the mesh
kirby pizza [action]      # Order, steal, or stash cheesy deep-dish pizza
kirby goblin              # Toggle full unhinged Goblin Mode
```

### H. Learning, Action Cards & Ledger
```bash
kirby cards               # List all known & learned action cards in active deck
kirby draw                # Draw a random action card with ASCII illustration
kirby play <card_id>      # Execute an action card across the mesh
kirby event <name>        # Emit system/user event & trigger Kirby's reactive response
kirby learn [count]       # Run autopoietic curiosity & learning cycles
kirby synthesize <a <b>   # Fuse two copy abilities into a new hybrid card
kirby ledger              # View evolutionary learning ledger and XP progression
kirby deck                # Inspect Kirby Motion Decision Deck JSON
```

### I. Web Portals & Verification
```bash
kirby multiverse | hub    # Kirby Multi-Verse & Squad Party Hub (:8088/multiverse)
kirby sanctuary | needs   # Kirby Needs & Wellbeing Sanctuary (:8088/needs)
kirby celestial           # Kirby Celestial Sanctuary 3D (:8088/celestial)
kirby swarm | megaswarm   # Kirby Mega-Swarm & Copy Ability Nexus (:8088/megaswarm)
kirby arena               # Multimodal Compression Agent Arena (:8088/arena)
kirby minions             # Minion Swarm DoF Platters 3D (:8088/minions)
kirby soundboard          # PixXL Foley Artist Soundboard (:8088/soundboard)
kirby haptics             # Multi-Touch Haptics Lab (:8088/haptics)
kirby test                # Run complete 18-stage automated verification test suite
```

### J. Windows 11 Desktop Companion (Operation Starfall Poyo)
```bash
kirby win11 [status]      # Status of Win11 Lappy (100.87.84.94), mesh bridge & portal
kirby win11 plan          # View Operation Starfall Poyo Master Plan & Spec
kirby win11 serve         # Web portal URLs for Win11 (:8088/win11)
kirby win11 package       # Bundle standalone Win11 zip package for deployment
```

---

## 2. 🎭 The Complete 10-Kirby Roster

Every Kirby in the multi-squad engine features distinct capabilities, personalities, and roles:

| # | Kirby | Emoji | Role & Special Ability | Personality |
| :- | :--- | :---: | :--- | :--- |
| 1 | **Kirby Prime** | 🌸 | Warp Star & Tappa Rhythm | Cheerful leader, insatiable appetite, courageous |
| 2 | **Noid Kirby** | 🍕 | Pizza Snatch & Port Glitch | Mischievous gremlin prankster, chaos summoner |
| 3 | **Magician Kirby** | 🎩 | Decoy Cursor & Tarot Pull | Flamboyant illusionist, mysterious, theatrical |
| 4 | **Ace Kirby** | ⚔️ | Ultra Sword & Megaman Laser | Stoic brawler `( ಠ ʖ̯ ಠ )`, compression gladiator |
| 5 | **Explorer Kirby** | 🧭 | Compass Waypoint & Relic Dowsing | Curious cartographer, ruins archaeologist |
| 6 | **Hypernova Kirby** | 🧹 | Black Hole Inhale & Zero Clutter | Cosmic janitor, dev cache vacuum cleaner |
| 7 | **Chaotix Kirby** | ⚡ | Neon Tethers & Particle Burst | Hyperactive, acoustic mechanical switch typist |
| 8 | **Keeby** | 💛 | Plasma Spark & Lightning Dash | Bubbly yellow sibling, warp speedrunner |
| 9 | **Freeze Kirby** | 💙 | Glacial Chill & CPU Cooling | Serene frost sage, cools CPU thermals to 34°C |
| 10 | **Shadow Kirby** | 🖤 | Mirror Shards & Shadow Step | Silent mirror guardian, watchful protector |

---

## 3. 🌐 Web Portals & Experiential Dashboards

Listening on `http://localhost:8088` (Dev Web Portal) and `http://localhost:8080` (Omni PyServe):

| Route | File Location | Key Capabilities |
| :--- | :--- | :--- |
| **`:8088/multiverse`** | [`kirby_multiverse_hub.html`](file:///mnt/shared/AntiGravity_Shared/kirby_multiverse_hub.html) | **Flagship Multi-Squad Hub**: 10-Kirby roster, 4-member active party, in-browser Samurai Quick Draw reflex minigame, live screen snapshot, feast button & audio-haptics. |
| **`:8088/needs`** | [`kirby_needs_sanctuary.html`](file:///mnt/shared/AntiGravity_Shared/kirby_needs_sanctuary.html) | **Kirby Needs & Wellbeing Sanctuary**: 8 Core Essential Needs meters, 10 Squad Cravings audit, 1-click care actions (Nap, Bubble Spa, Hug, Feng Shui, Chill, Auto-Care). |
| **`:8088/tappa`** | [`kirby_projectm_tappa.html`](file:///mnt/shared/AntiGravity_Shared/kirby_projectm_tappa.html) | **Kirby x ProjectM Studio**: WebGL Milkdrop shaders, Tap Tempo BPM, tactile LRA haptics, 808 beat generator & live Mic. |
| **`:8088/celestial`** | [`kirby_celestial_sanctuary_3d.html`](file:///mnt/shared/antigravity_hub/public/kirby_celestial_sanctuary_3d.html) | Three.js floating celestial islands, volumetric cloudscape, star-spit physics. |
| **`:8088/megaswarm`** | [`kirby_mega_swarm_copy_ability_nexus.html`](file:///mnt/shared/antigravity_compendium/public/kirby_mega_swarm_copy_ability_nexus.html) | Interactive 3D world with 100+ copy ability transformations. |
| **`:8088/arena`** | [`multimodal_compression_agent_mesh_arena.html`](file:///mnt/shared/AntiGravity_Shared/multimodal_compression_agent_mesh_arena.html) | 3D Arena starring Ace Kirby `( ಠ ʖ̯ ಠ )`, Mettaurs, and Megaman X Lasers. |
| **`:8088/soundboard`** | [`pixxl_soundboard.html`](file:///mnt/shared/AntiGravity_Shared/pixxl_soundboard.html) | Synthesizes Kirby Inhale Vortex, Star Spit Pop, Float Flutter, Warp Star Engine. |
| **`:8088/haptics`** | [`pixxl_multitouch_haptics_lab.html`](file:///mnt/shared/AntiGravity_Shared/pixxl_multitouch_haptics_lab.html) | Hardware LRA tactile responses and touch gesture sandbox. |
| **`:8088/minions`** | [`minion_swarm_dof_platters_3d.html`](file:///mnt/shared/antigravity_hub/public/minion_swarm_dof_platters_3d.html) | Depth-of-Field instanced minion horde benchmark. |
| **`:8088/noid`** | [`pixxl_kirby_noid_annoy.html`](file:///mnt/shared/AntiGravity_Shared/pixxl_kirby_noid_annoy.html) | The Noid Gremlin chaos deck, pizza delivery tracker & prank console. |
| **`:8088/win11`** | [`kirby_win11_companion.html`](file:///mnt/shared/AntiGravity_Shared/win11_kirby/kirby_win11_companion.html) | **Windows 11 Lappy Companion**: Warp Star fly-in, star departure, eye-tracking avatar, Pomodoro, Inhale clipboard cleaner, Poyo soundboard & live Node-A mesh telemetry. |

---

## 4. ⚔️ Minigames & Reflex Duels

### Samurai Kirby Quick Draw (`kirby samurai` | `kirby_quick_draw.py`)
- Recreates the classic reflex showdown with microsecond accuracy via `time.perf_counter()`.
- 5 Iconic Opponents + 1 Secret Boss:
  1. **Waddle Doo** (~380ms)
  2. **Whispy Woods** (~315ms)
  3. **Bonkers Ape** (~255ms)
  4. **King Dedede** (~205ms)
  5. **Meta Knight** (~165ms)
  6. **[SECRET] Noid Gremlin Kirby** (~135ms!)
- False start penalty: drawing early triggers a DQ!
- High scores tracked in [`.kirby_quick_draw_scores.json`](file:///mnt/shared/AntiGravity_Shared/.kirby_quick_draw_scores.json).

### Kirby Star Catcher (`kirby play` | `kirby_star_catcher.py`)
- 18 FPS ANSI double-buffered terminal arcade game.
- Catch falling stars, Maxim Tomatoes, and Star Shards while dodging glitch blocks.
- Persistent scores tracked in [`.kirby_high_score.json`](file:///mnt/shared/AntiGravity_Shared/.kirby_high_score.json).

### Chaotix Typey Arena (`kirby typey` | `kirby_chaotix_typey.py`)
- Ephemeral raw keyboard typing physics sandbox with 120s TTL RAM session.
- Real-time particle tethers, bouncing ASCII sparks, and Cherry switch audio acoustics.

---

## 5. 🎩 Magician Kirby & Tac Sleight-of-Hand Engine

Implements the 4-Act Cinematic Screenplay Director ([`kirby_magician_tac.py`](file:///mnt/shared/AntiGravity_Shared/scripts/kirby_magician_tac.py)):
- **Act I: The Setup**: Magician Kirby bows; Tac the Cat creeps along the status bar.
- **Act II: The Misdirection**: Star wand flourish swaps the operator pointer with a decoy cursor.
- **Act III: The Prestige**: Catapults focus into hot input zone & reveals Tarot Card from velvet top hat.
- **Act IV: Resolution**: `✨ Presto Chango! ✨` restores everything with a shower of stars & ledger XP.
- **Tarot Deck**: The Star (XVII), The Magician (I), The Chariot (VII), The Fool (0), The Hermit (IX), The Wheel (X).

---

## 6. 📱 Native Android Floating Overlay & Services

- **Overlay Service**: [`KirbyNativeOverlayService.kt`](file:///mnt/shared/AntiGravity_Shared/android_hud_app/app/src/main/java/com/antigravity/mindmesh/kirby/KirbyNativeOverlayService.kt)
- **Visitor Access Point**: [`KirbyVisitorAccessPointService.kt`](file:///mnt/shared/AntiGravity_Shared/android_hud_app/app/src/main/java/com/antigravity/mindmesh/kirby/KirbyVisitorAccessPointService.kt)
- **Live Snapshot**: [`kirby_live_screen.png`](file:///mnt/shared/kirby_live_screen.png)

### Hardware LRA Touch Gestures
- **1-Finger Drag**: Move Kirby anywhere on screen with `dragPickup` haptics.
- **1-Finger Release**: Snaps Kirby to safe boundary margins with `dockSnap` haptics.
- **2-Finger Pinch**: Scale Kirby smoothly from 0.65x to 2.50x with `detentTick`.
- **2-Finger Twist**: Rotate Kirby 0° to 360° with 30° ratchet notches.
- **2-Finger Double-Tap**: Cycle moods & facial expressions (`doubleClick`).
- **3-Finger Tap**: Display live phone telemetry toast (`heavyThud`).

---

## 7. 🧪 Automated 18-Stage Verification Suite

Run at any time:
```bash
kirby test
```
Verifies all 18 ecosystem subsystems:
1. Star Catcher Headless Simulation
2. Oracle of Poyo Wisdom Engine
3. Kirby Studio Micro-Gem Generator
4. Dev Web Portal Endpoints (including `/celestial`, `/megaswarm`, `/arena`, `/minions`, `/soundboard`, `/haptics`, `/tappa`, `/noid`, `/multiverse`, `/needs`, etc.)
5. Omni PyServe Multi-Port Endpoints
6. Android Overlay & Visitor Access Point
7. Kirby Motion Decision Deck (37 cards)
8. Action Cards Registry & Deck (83 cards)
9. Ability Fusion & Synthesis Engine
10. Reactive Event Response Matrix
11. Evolutionary Learning Ledger (140+ entries)
12. Tamagotchi Pet Care & Feeding Engine
13. Dream Land Expeditions Quest Engine
14. Boss Arena Colosseum Engine
15. Hypernova System Cleaner Engine
16. Multi-Squad Party, Samurai Quick Draw & Magician Engines
17. Kirby Holistic Needs, Caretaker Duo (Dee & Kawasaki) & Mutual Care Engine
18. **Windows 11 Desktop Companion & Invasion Suite (Operation Starfall Poyo)**

---

## 8. 💻 Windows 11 Desktop Companion (Operation Starfall Poyo)

Target: `ajr-win11-lappy` (`100.87.84.94`) • Blueprint: [`KIRBY_WIN11_INVASION_PLAN.md`](file:///home/droid/.gemini/antigravity-cli/brain/b849097c-aa2f-49f6-99ad-79da16632b54/KIRBY_WIN11_INVASION_PLAN.md)

### Key Capabilities & "Just Kirby Solo" Directive:
- **Cinematic Warp Star Fly-In**: Kirby streaks in from off-screen on a golden glowing Warp Star with supersonic Doppler whoosh audio, lands with squish hop physics, and the star flies away into deep space.
- **Desktop Habitation**: Wanders along the taskbar, perches on active windows, tracks your mouse cursor with live animated eyes, bobs to your typing rhythm, and curls up on a Dream Cloud when idle.
- **Interactive Kirby Toolbox**:
  1. **Quick Launcher**: Instant links to dev tools, terminal, and mesh portals.
  2. **Maxim Tomato Pomodoro**: 25m/5m focus sprint countdown with cheering jingles.
  3. **Hypernova Inhale Cleaner**: Formats messy JSON, trims spaces, unescapes strings.
  4. **Poyo Soundboard**: 12+ real-time synthesized procedural sound effects.
  5. **Live Mesh Telemetry**: Real-time battery, thermal, and TPU load from Pixel 9 Pro XL.
  6. **Care Sanctuary**: Hydration, posture, and 20-20-20 eye break reminders.
  7. **Petting & Snacks**: Feed Maxim Tomatoes or scratch Kirby's head for happy purrs!

### Launch Vectors on Windows 11:
- **1-Click Batch**: Double-click [`launch_kirby_win11.bat`](file:///mnt/shared/AntiGravity_Shared/win11_kirby/launch_kirby_win11.bat).
- **Native WPF Overlay**: `powershell.exe -ExecutionPolicy Bypass -File .\kirby_win11_invasion.ps1` (zero install).
- **Modern Edge Portal**: Navigate to `http://100.121.245.47:8088/win11` in Edge or Chrome.


