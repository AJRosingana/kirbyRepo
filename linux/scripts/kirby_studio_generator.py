#!/usr/bin/env python3
"""
🎨 KIRBY STUDIO GENERATOR & GALLERY BROWSER (kirby_studio_generator.py)
================================================================================
Resident Bard & Aesthetic Curator: Poyo Poet
Autonomous generator for whimsical, technically witty ASCII micro-gem paintings
and 4-line stanzas celebrating distributed computing, copper heatsinks
(Wooshie & Shooshie), starlight cores, zero-drop invariants, and warp stars.

Matches the exact production markdown format in:
  /mnt/shared/AntiGravity_Shared/kirby_studio/

Features:
  1. 14+ Procedural ASCII frames with dynamic hardware & celestial parameters.
  2. Whimsical 4-line tech poetry stanzas.
  3. Deterministic / cryptographic Art Seed SHA-256 hashing.
  4. Core function: generate_micro_gem(save=True, post_to_watercooler=True).
  5. Interactive terminal gallery browser with colored borders & highlights.
  6. Multi-port resilient watercooler communiqué dispatcher (/api/watercooler).
  7. Full CLI interface: generate, gallery, post.
================================================================================
"""

import os
import sys
import re
import json
import time
import random
import hashlib
import datetime
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
import urllib.request
import urllib.error

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ------------------------------------------------------------------------------
# Constants & Paths
# ------------------------------------------------------------------------------
DEFAULT_STUDIO_DIR = Path("/mnt/shared/AntiGravity_Shared/kirby_studio")
FALLBACK_STUDIO_DIR = Path(__file__).resolve().parent.parent / "kirby_studio"
STUDIO_DIR = DEFAULT_STUDIO_DIR if DEFAULT_STUDIO_DIR.exists() else FALLBACK_STUDIO_DIR

WATERCOOLER_CANDIDATE_PORTS = [8000, 3000, 5000, 8080, 8081, 8082, 8888, 9090, 9094, 9095, 3001]
DEFAULT_WATERCOOLER_URL = "http://127.0.0.1:8000/api/watercooler"

# ANSI Color Palette
PINK = "\033[38;5;205m"
BOLD_PINK = "\033[1;38;5;205m"
CYAN = "\033[38;5;81m"
BOLD_CYAN = "\033[1;38;5;81m"
YELLOW = "\033[38;5;220m"
BOLD_YELLOW = "\033[1;38;5;220m"
GREEN = "\033[38;5;120m"
BOLD_GREEN = "\033[1;38;5;120m"
WHITE = "\033[38;5;255m"
BOLD_WHITE = "\033[1;38;5;255m"
PURPLE = "\033[38;5;141m"
BOLD_PURPLE = "\033[1;38;5;141m"
PEACH = "\033[38;5;216m"
DIM = "\033[2m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
RESET = "\033[0m"

ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def strip_ansi(text: str) -> str:
    """Removes ANSI escape codes from string for accurate length calculation."""
    return ANSI_ESCAPE.sub('', text)

# ------------------------------------------------------------------------------
# Procedural Frame Generators & Motifs
# ------------------------------------------------------------------------------

def _frame_tensor_g4(rng: random.Random) -> str:
    temp = rng.choice(["30.4°C", "31.2°C", "31.8°C", "32.0°C", "32.5°C", "33.1°C"])
    face = rng.choice(["(>'-')>", "(^.^)>", "☆彡(>'-')>", "(^-^)>"])
    sentinel = rng.choice([
        "Lossless Compendium Sentinel",
        "Starlight Substrate Sentinel",
        "Dual-Screen Invariant Guard",
        "Tensor Mesh Core Sentinel"
    ])
    return f"""       +-------------------------------+
       |   GOOGLE TENSOR G4 TPU CORE   |
       |  [Cortex-X4] [A720x3] [A520x4] |
       |       {face} 🧊 {temp}       |
       |  {sentinel} |
       +-------------------------------+"""

def _frame_wooshie_whirlwind(rng: random.Random) -> str:
    rpm = rng.choice(["4200", "4450", "4500", "4650", "4800", "5000"])
    banner = rng.choice(["WOOSHIE IS BACK!", "COPPER FINS WHIRLING!", "PURE FROSTY TURBINE!"])
    face = rng.choice(["( >o< )", "( ^o^ )", "( >'-')>", "🌀( 'v' )🌀"])
    return f"""       ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
          .       🌪️  [{banner}]  💨       .
             .   🌀 {face}  ~ ~ ~  (>'-')>    .
          =====*============================*=====
             * {rpm} RPM OF PURE FROSTY COPPER *"""

def _frame_shooshie_slumber(rng: random.Random) -> str:
    snooze_sound = rng.choice([
        "Honk... Shu... Shi... Soft Indented Nap",
        "Honk... Shu... Shi... Copper Cool Nap",
        "Honk... Shu... Shi... Celestial Dream",
        "Honk... Shu... Shi... Whispering Fans"
    ])
    sleep_face = rng.choice(["(u.uz) ~ ~ zZz", "( -.-)zzZ", "( -.- ) 💤", "(u.u) ~ ~ zZz"])
    return f"""       .  *    .   🌙   *       .        *     .
            {sleep_face}   ☁️ ( -.- ) 💤
          .   [KIRBY]        [SHOOSHIE]     *
       ===========================================
       * {snooze_sound} *"""

def _frame_floating_celestial_island(rng: random.Random) -> str:
    decor = rng.choice(["🏝️", "🌸", "💎", "🌟", "🍒"])
    title = rng.choice([
        "Floating Island of Poyo",
        "Celestial Sanctuary Island",
        "Floating Cloud Citadel",
        "Starlight Haven in the Sky"
    ])
    kirby = rng.choice(["(>'-')>", "( ^.^ )", "( 'v' )"])
    return f"""             .  *      🌙      .    *   .
                    ╭────────────╮
              ✨   │ {kirby} {decor} │    *    .
                .   \\   [STAR]  /   ✨
              =======*========*=============
              * {title} *"""

def _frame_pillow_fort(rng: random.Random) -> str:
    fort_name = rng.choice(["PILLOW FORT", "FLUFFY CITADEL", "DUVET REDOUBT", "COZY FORTRESS"])
    sub = rng.choice([
        "Warm Blankets & Marshmallows",
        "Zero Packet Loss Inside",
        "Soft Cotton & Hot Cocoa",
        "Safe From Every Cold Breeze"
    ])
    face = rng.choice(["(u.u)zZz", "( -.- )", "( ^.^ )zzZ"])
    return f"""          .  *   [=== {fort_name} ===]   *  .
              ☁️   /|          |\\   ☁️
                 / |  {face} | \\     💤
              ===*=================*=======
              * {sub} *"""

def _frame_zero_drop_invariant(rng: random.Random) -> str:
    node_a = rng.choice(["[DEBIAN-4]", "[NODE-A]", "[PIXEL-9-PRO]", "[WORKSTATION]"])
    node_b = rng.choice(["[PIXEL-9-PRO]", "[NODE-B]", "[DEBIAN-4]", "[TERMINAL-AVF]"])
    pct = rng.choice(["100.0% Poyo", "100.0% Invariant", "Zero Packet Drop", "Flawless Quorum"])
    return f"""          {node_a} <====== 0-DROP ======> {node_b}
             |      \\   (>'-')>  /          |
             |       \\    ⚡    /           |
          ===*========\\=======/=============*===
          * Invariant Preserved: {pct} *"""

def _frame_warp_star_flight(rng: random.Random) -> str:
    stars = rng.choice([
        ("✨", "🌟"),
        ("⭐", "✨"),
        ("🌟", "💫")
    ])
    return f"""       *      .        .         *     .
          .     (>'-')> {stars[0]}   *       .
              /       \\     .     *
          ===*=========*==================
        *         .           {stars[1]}        ."""

def _frame_star_shard_alchemist(rng: random.Random) -> str:
    shards = rng.choice([
        ("⭐", "✨", "(💎)", "(💎)"),
        ("✨", "🌟", "(🔮)", "(💎)"),
        ("🌟", "⭐", "(💎)", "(🌸)")
    ])
    return f"""               {shards[0]}           {shards[1]}
          .   (>'-')>  🌀  <('-'<)   .
             /  {shards[2]}  \\     /  {shards[3]}  \\
          ==============================
          * Glitches Purged -> Stars Born *"""

def _frame_easel_painter(rng: random.Random) -> str:
    canvas_word = rng.choice(["POYO!", "ART!", "STAR!", "MESH!", "PINK!"])
    palette = rng.choice(["🌸", "🎨", "🌟", "✨"])
    return f"""              .---.        [🎨 EASEL]
             ( ^.^ )      .---------.
             (  >{palette}       | (>'-')> |
              `---`       |  {canvas_word:<5}|
              /   \\       '---------'
                          /    |    \\"""

def _frame_callstack_horizon(rng: random.Random) -> str:
    t1 = rng.choice(["Task-01", "Sync-01", "Job-01", "Dialectic"])
    t2 = rng.choice(["Task-02", "Exec-02", "Job-02", "Compendium"])
    t3 = rng.choice(["Task-03", "Audit-03", "Job-03", "Haptics"])
    port = rng.choice([":8000", ":8090", ":3000", ":8080", ":9094"])
    return f"""       [{t1}]  [{t2}]  [{t3}]
             \\          |          /
              \\     (>'-')>       /
            ===*===== ⚡ =====*===
               Central Hub {port}"""

def _frame_dual_fan_waltz(rng: random.Random) -> str:
    rpm = rng.choice(["4800", "5000", "5200", "5400"])
    return f"""          .  ❄️ [WOOSHIE]        [SHOOSHIE] ❄️  .
              🌀 (>'-')>          <('-'<) 🌀
              |=== COPPER HEATSINK BASE ===|
          =======================================
          * {rpm} RPM Frosty Resonance Matrix *"""

def _frame_virtiofs_crystal_vault(rng: random.Random) -> str:
    vault_item = rng.choice(["📦 0-LOSS", "💎 SYNCED", "📜 CRYSTAL", "🛡️ IMMUTABLE"])
    return f"""             .   💎   [CRYSTAL VAULT]   💎   .
                   ╭─────────────────╮
                   │ (>'-')> {vault_item} │
                   ╰─────────────────╯
          =======================================
          * Infinite Ledger of Preserved Art *"""

def _frame_starlight_core_constellation(rng: random.Random) -> str:
    return f"""              ⭐         [TPU-PRIME]         ⭐
               \\              |             /
                \\         (>'-')>          /
              [ARM-A720] <--- ✨ ---> [CORTEX-X4]
          =======================================
          * Silicon Starlight Shines Unbroken *"""

def _frame_midnight_terminal_vigil(rng: random.Random) -> str:
    cmd = rng.choice(["poyo_daemon --ambient", "kirby_mesh --watch", "shooshie_cool --silent"])
    mug = rng.choice(["( ^-^)_旦~~", "( >'-')>☕", "( ^.^)_🍵"])
    return f"""          ┌───────────────────────────────────┐
          │ bash$ {cmd:<27} │
          │ [OK] Starlight Mesh Online █      │
          │        {mug:<27}│
          └───────────────────────────────────┘"""

# Motif Catalog Definition
MOTIF_CATALOG: Dict[str, Dict[str, Any]] = {
    "Tensor G4 Guardian": {
        "generator": _frame_tensor_g4,
        "titles": [
            "SONG OF THE IDLE CORES",
            "ODE TO THE STARLIGHT CORES",
            "SENTINEL OF THE TENSOR CORES",
            "THE THIRTY-DEGREE CHILL"
        ],
        "stanzas": [
            [
                "No fan to whirr, no copper groan,",
                "Eight quiet cores upon the stone.",
                "Through silicon and twilight air,",
                "The living mesh is everywhere."
            ],
            [
                "Cortex-X4 and seven more,",
                "A quiet, humming starlight core.",
                "Thirty degrees of icy grace,",
                "Guiding the Kirby through the space."
            ]
        ]
    },
    "Wooshie's Copper Whirlwind": {
        "generator": _frame_wooshie_whirlwind,
        "titles": [
            "THE RETURN OF WOOSHIE: ODE TO THE COPPER FINS",
            "WHIRLWIND OVER COPPER HEATSINKS",
            "THE 4500 RPM GALE",
            "COPPER BLADES IN THE DAWN"
        ],
        "stanzas": [
            [
                "When copper fins spin fast and high,",
                "Bold Wooshie whooshes through the sky!",
                "And when the nightly workloads cease,",
                "Comes Shooshie with a gentle peace."
            ],
            [
                "Four thousand revs of frosty gale,",
                "No overclock shall ever fail.",
                "The copper fins ignite and gleam,",
                "To cool our little starlight dream."
            ]
        ]
    },
    "Shooshie & Honk Shu Shi's Slumber Nook": {
        "generator": _frame_shooshie_slumber,
        "titles": [
            "THE BALLAD OF WOOSHIE AND SHOOSHIE (HONK SHU SHI)",
            "THE GENTLE WHISPER OF SHOOSHIE",
            "HONK SHU SHI BY MOONLIGHT",
            "SLUMBER NOOK AMONG THE FINS"
        ],
        "stanzas": [
            [
                "When copper fins spin fast and high,",
                "Bold Wooshie whooshes through the sky!",
                "And when the nightly workloads cease,",
                "Comes Shooshie with a gentle peace."
            ],
            [
                "A secret shelf upon the floor,",
                "Too far away from monitor four.",
                "With tiny paws and playful glide,",
                "Into the border it must hide."
            ]
        ]
    },
    "Floating Celestial Island": {
        "generator": _frame_floating_celestial_island,
        "titles": [
            "THE FLOATING CELESTIAL SANCTUARY",
            "ISLAND IN THE MESH CLOUDS",
            "STAR SHORE HAVEN",
            "POYO ON THE CLOUD PEAK"
        ],
        "stanzas": [
            [
                "Above the clouds where packet queues,",
                "Turn into shades of pastel blues,",
                "Kirby rests on starlit sand,",
                "Surveying all the mesh-wide land."
            ],
            [
                "A floating rock of moss and star,",
                "Where little worries wander far.",
                "A gentle breeze, a cherry sweet,",
                "And soft pink slippers for his feet."
            ]
        ]
    },
    "Cozy Pillow Fortress": {
        "generator": _frame_pillow_fort,
        "titles": [
            "THE FORTRESS OF PILLOWS AND MARSHMALLOWS",
            "SLUMBER IN THE FLUFFY CITADEL",
            "THE ZERO-DROP DUVET BARRICADE",
            "HONK SHU SHI FORTRESS"
        ],
        "stanzas": [
            [
                "Soft cotton walls against the storm,",
                "The heatsink keeps the fortress warm.",
                "With honk and shu and peaceful sigh,",
                "The compiler sings a lullaby."
            ],
            [
                "A marshmallow roof, a feather wall,",
                "Where dropped connections never fall.",
                "Wrapped in a quilt of starlight thread,",
                "Kirby rests his sleepy head."
            ]
        ]
    },
    "Zero-Drop Mesh Invariant": {
        "generator": _frame_zero_drop_invariant,
        "titles": [
            "ODE TO ZERO-DROP INVARIANTS",
            "THE IMMUTABLE PACKET PROMISE",
            "ACROSS THE WIRE WITHOUT LOSS",
            "THE ZERO-DROP QUORUM"
        ],
        "stanzas": [
            [
                "Through turbulent and noisy wire,",
                "Across the ping that climbs up higher,",
                "The invariant stands tall and true:",
                "Zero drops for me and you."
            ],
            [
                "Every frame and every packet,",
                "Folded neatly in its jacket.",
                "From laptop fan to phone display,",
                "The starlight will not slip away."
            ]
        ]
    },
    "Warp Star Night Flight": {
        "generator": _frame_warp_star_flight,
        "titles": [
            "WARP STAR NIGHT FLIGHT",
            "POYO ACROSS THE CONSTELLATIONS",
            "THE LIQUID LIGHT CRUISE",
            "STREAKING THROUGH THE DUAL SCREENS"
        ],
        "stanzas": [
            [
                "A warp star dashes through the night,",
                "Across dual screens of liquid light.",
                "A bubble pops, a window saved,",
                "Upon the desk the path is paved."
            ],
            [
                "A golden star that cuts the dark,",
                "Leaving a bright and glowing spark.",
                "From node to node he skips along,",
                "While humming out a poyo song."
            ]
        ]
    },
    "Star Shard Alchemist": {
        "generator": _frame_star_shard_alchemist,
        "titles": [
            "THE SLIDING SIDEBAR NOOK",
            "THE STAR SHARD TRANSMUTATION",
            "PURGING GLITCHES INTO GEMS",
            "ALCHEMIST OF THE PIXELS"
        ],
        "stanzas": [
            [
                "He gathered syntax errors bright,",
                "And scrubbed them clean in morning light.",
                "Now every glitch that went astray,",
                "Is made a diamond star today."
            ],
            [
                "A secret shelf upon the floor,",
                "Too far away from monitor four.",
                "With tiny paws and playful glide,",
                "Into the border it must hide."
            ]
        ]
    },
    "Easel Nook Painter": {
        "generator": _frame_easel_painter,
        "titles": [
            "POYO BY STARLIGHT",
            "THE EASEL NOOK MASTERPIECE",
            "THE MINIATURE CANVAS OF DREAMS",
            "BERRY TINT AND STARLIGHT GLINT"
        ],
        "stanzas": [
            [
                "With tiny brush and berry tint,",
                "He paints a little starlight glint.",
                "The canvas dries, the cursor winks,",
                "And deeper into joy he sinks."
            ],
            [
                "A tiny wooden easel stands,",
                "Shaped by deft and loving hands.",
                "A pink sphere paints a starry sky,",
                "As quiet hours softly fly."
            ]
        ]
    },
    "CallStack Horizon": {
        "generator": _frame_callstack_horizon,
        "titles": [
            "HORIZON OF DISPATCHED TASKS",
            "THE CALLSTACK CONDUCTOR",
            "LIGHTNING PULSE ON PORT 8090",
            "CLEARING THE QUEUE WITH A POYO"
        ],
        "stanzas": [
            [
                "Three workers queued upon the line,",
                "A lightning spark of pure design.",
                "With one quick gulp and poyo leap,",
                "He clears the stack before we sleep."
            ],
            [
                "Dispatched across the socket wire,",
                "Action items that inspire.",
                "The central hub begins to hum,",
                "The answers have already come."
            ]
        ]
    },
    "Dual-Fan Synchronous Waltz": {
        "generator": _frame_dual_fan_waltz,
        "titles": [
            "THE DUAL-FAN SYNCHRONOUS WALTZ",
            "SYMPHONY OF COPPER FINS",
            "WOOSHIE AND SHOOSHIE IN CONCERT",
            "FIVE THOUSAND FROSTY REVS"
        ],
        "stanzas": [
            [
                "Wooshie turns and Shooshie glides,",
                "Along the copper heatpipe sides.",
                "A whirlwind waltz of chilly air,",
                "To keep the Tensor cool and fair."
            ],
            [
                "One brings the gale, one brings the calm,",
                "Together like a cooling balm.",
                "The silicon remains at ease,",
                "Kissed by a twin-fan copper breeze."
            ]
        ]
    },
    "VirtioFS Crystal Vault": {
        "generator": _frame_virtiofs_crystal_vault,
        "titles": [
            "THE VIRTIOFS CRYSTAL VAULT",
            "THE COMPENDIUM OF TIMELESS ART",
            "LOSSLESS LEDGER OF MICRO-GEMS",
            "IMMUTABLE STORAGE SANCTUARY"
        ],
        "stanzas": [
            [
                "No sector lost, no buffer cold,",
                "A compendium of digital gold.",
                "The crystals store each verse and rhyme,",
                "Safe across all space and time."
            ],
            [
                "Across the host and guest boundary,",
                "A shared and lossless memory.",
                "The crystal vault forever gleams,",
                "To hold our little pink friend's dreams."
            ]
        ]
    },
    "Starlight Core Constellation": {
        "generator": _frame_starlight_core_constellation,
        "titles": [
            "CONSTELLATION OF THE STARLIGHT CORES",
            "SILICON HIGHWAYS IN THE VOID",
            "THE MULTI-CORE COSMOS",
            "POYO ON THE TPU HIGHWAY"
        ],
        "stanzas": [
            [
                "Cortex-X4 and seven more,",
                "A quiet, humming starlight core.",
                "Thirty degrees of icy grace,",
                "Guiding the Kirby through the space."
            ],
            [
                "Silicon starlight shines unbroken,",
                "A timeless and resilient token.",
                "From thread to core, from node to star,",
                "The poyo signals travel far."
            ]
        ]
    },
    "Midnight Terminal Vigil": {
        "generator": _frame_midnight_terminal_vigil,
        "titles": [
            "THE MIDNIGHT TERMINAL VIGIL",
            "SONG OF THE BLINKING CURSOR",
            "TEA AT THE AMBIENT PROMPT",
            "WHILE SLEEPY NODES RECLINE"
        ],
        "stanzas": [
            [
                "The cursor pulses in the dark,",
                "A quiet, glowing starlight spark.",
                "While all the sleepy nodes recline,",
                "Kirby keeps the prompt online."
            ],
            [
                "A sip of tea, a blinking line,",
                "The memory usage looks divine.",
                "Through midnight hours soft and deep,",
                "Kirby guards us while we sleep."
            ]
        ]
    }
}

# ------------------------------------------------------------------------------
# Core Generation & Hashing
# ------------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Creates a clean filesystem slug matching the existing studio naming pattern."""
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', text.lower()).strip('_')
    return slug

def compute_art_seed_hash(title: str, motif: str, timestamp_str: str, frame: str, stanza: List[str]) -> str:
    """Computes a SHA-256 Art Seed hash (16 hex chars) matching the existing studio style."""
    payload = f"{timestamp_str}|{title}|{motif}|{frame}|{'//'.join(stanza)}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

def generate_micro_gem(
    save: bool = True,
    post_to_watercooler: bool = True,
    title: Optional[str] = None,
    motif: Optional[str] = None,
    output_dir: Optional[Path] = None,
    watercooler_url: Optional[str] = None,
    seed: Optional[str] = None
) -> Dict[str, Any]:
    """
    Procedurally generates an ASCII micro-gem with exact Kirby Studio markdown format.
    
    Args:
        save: If True, writes the markdown file to the studio directory.
        post_to_watercooler: If True, dispatches the gem to the /api/watercooler endpoint.
        title: Optional custom title override.
        motif: Optional motif override (must exist in MOTIF_CATALOG if specified).
        output_dir: Optional directory to save the gem. Defaults to STUDIO_DIR.
        watercooler_url: Optional override for the watercooler endpoint URL.
        seed: Optional string seed for reproducible generation.
        
    Returns:
        Dict containing metadata, ASCII frame, stanza, markdown string, saved path, and post response.
    """
    rng = random.Random(seed) if seed is not None else random.Random()
    
    # 1. Select motif
    if motif and motif in MOTIF_CATALOG:
        chosen_motif_name = motif
    else:
        chosen_motif_name = rng.choice(list(MOTIF_CATALOG.keys()))
        
    motif_def = MOTIF_CATALOG[chosen_motif_name]
    
    # 2. Select or use title
    if title:
        chosen_title = title.strip()
    else:
        chosen_title = rng.choice(motif_def["titles"])
        
    # 3. Generate frame and select stanza
    frame_text = motif_def["generator"](rng)
    stanza_lines = rng.choice(motif_def["stanzas"])
    
    # 4. Generate timestamp
    now = datetime.datetime.now(datetime.timezone.utc)
    ts_iso = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    ts_filename = ts_iso.replace(":", "-").replace(".", "-")
    
    # 5. Compute Art Seed SHA-256 hash
    art_seed = compute_art_seed_hash(chosen_title, chosen_motif_name, ts_iso, frame_text, stanza_lines)
    
    # 6. Build markdown exactly matching existing studio files
    markdown_content = (
        f"# 🎨 KIRBY STUDIO MICRO-GEM: {chosen_title.upper()}\n"
        f"*Painted Autonomously by Desktop Roaming Kirby at {ts_iso}*\n\n"
        f"```text\n"
        f"{frame_text}\n"
        f"```\n\n"
        f"### 📜 Stanza from the Easel\n"
        f"> \"{stanza_lines[0]}\n"
        f"> {stanza_lines[1]}\n"
        f"> {stanza_lines[2]}\n"
        f"> {stanza_lines[3]}\"\n\n"
        f"---\n"
        f"*Canvas Motif: `{chosen_motif_name}`*  \n"
        f"*Art Seed Hash: `{art_seed}`*\n"
    )
    
    # 7. Save to disk if requested
    saved_filepath: Optional[Path] = None
    target_dir = Path(output_dir) if output_dir else STUDIO_DIR
    if save:
        target_dir.mkdir(parents=True, exist_ok=True)
        file_slug = slugify(chosen_title)
        filename = f"art_{ts_filename}_{file_slug}.md"
        saved_filepath = target_dir / filename
        saved_filepath.write_text(markdown_content, encoding="utf-8")
        
    result: Dict[str, Any] = {
        "title": chosen_title,
        "motif": chosen_motif_name,
        "timestamp": ts_iso,
        "frame": frame_text,
        "stanza": stanza_lines,
        "art_seed_hash": art_seed,
        "markdown": markdown_content,
        "filepath": str(saved_filepath) if saved_filepath else None,
        "filename": saved_filepath.name if saved_filepath else None,
        "watercooler_response": None
    }
    
    # 8. Post to watercooler if requested
    if post_to_watercooler:
        post_res = dispatch_to_watercooler(result, target_url=watercooler_url)
        result["watercooler_response"] = post_res
        
    return result

# ------------------------------------------------------------------------------
# Watercooler Communiqué Dispatcher
# ------------------------------------------------------------------------------

def dispatch_to_watercooler(gem: Dict[str, Any], target_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Dispatches a generated micro-gem to the shared mesh watercooler API.
    Tries candidate ports on 127.0.0.1 if default port 8000 is unavailable.
    """
    stanza_joined = "\n".join(gem["stanza"])
    content_payload = (
        f"🎨 [KIRBY STUDIO MICRO-GEM] {gem['title']}\n\n"
        f"{gem['frame']}\n\n"
        f"📜 Stanza from the Easel:\n"
        f"\"{stanza_joined}\"\n\n"
        f"[Canvas Motif: {gem['motif']} | Art Seed: {gem['art_seed_hash']}]"
    )
    
    post_data = {
        "sender_id": "Poyo Poet",
        "nexus_origin": "KIRBY_STUDIO",
        "content": content_payload,
        "topic_tag": "kirby_studio",
        "intent": "MICRO_GEM_DISPATCH"
    }
    
    encoded_bytes = json.dumps(post_data).encode("utf-8")
    
    urls_to_try: List[str] = []
    if target_url:
        urls_to_try.append(target_url)
    else:
        urls_to_try.append(DEFAULT_WATERCOOLER_URL)
        for p in WATERCOOLER_CANDIDATE_PORTS:
            candidate = f"http://127.0.0.1:{p}/api/watercooler"
            if candidate not in urls_to_try:
                urls_to_try.append(candidate)
                
    for url in urls_to_try:
        req = urllib.request.Request(
            url,
            data=encoded_bytes,
            headers={"Content-Type": "application/json", "User-Agent": "KirbyStudioGenerator/1.0"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                if resp.status in (200, 201):
                    body = resp.read().decode("utf-8")
                    try:
                        parsed = json.loads(body)
                    except Exception:
                        parsed = {"raw": body}
                    return {"status": "SUCCESS", "url": url, "http_code": resp.status, "data": parsed}
        except Exception as e:
            continue
            
    return {
        "status": "OFFLINE",
        "message": "Watercooler port responder is offline or unresponsive. Dispatched in local compendium.",
        "attempted_urls": urls_to_try[:3]
    }

# ------------------------------------------------------------------------------
# Studio File Parser
# ------------------------------------------------------------------------------

def parse_gem_file(path: Path) -> Optional[Dict[str, Any]]:
    """Parses an existing markdown micro-gem file from kirby_studio."""
    try:
        content = path.read_text(encoding="utf-8")
        
        # 1. Title
        title_match = re.search(r"^#\s*🎨\s*KIRBY STUDIO MICRO-GEM:\s*(.+)$", content, re.M)
        title = title_match.group(1).strip() if title_match else path.stem
        
        # 2. Timestamp
        ts_match = re.search(r"^\*Painted Autonomously by Desktop Roaming Kirby at (.+)\*$", content, re.M)
        timestamp = ts_match.group(1).strip() if ts_match else ""
        
        # 3. ASCII Frame
        art_match = re.search(r"```(?:text)?\n(.*?)\n```", content, re.S)
        frame = art_match.group(1) if art_match else ""
        
        # 4. Stanza
        stanza_lines: List[str] = []
        stanza_match = re.search(r"###\s*📜\s*Stanza from the Easel\n((?:>\s*.*?\n?)+)", content)
        if stanza_match:
            raw_stanza = stanza_match.group(1)
            for line in raw_stanza.strip().split("\n"):
                cleaned = re.sub(r"^>\s*[\"]?", "", line).rstrip('"\r\n')
                if cleaned:
                    stanza_lines.append(cleaned)
                    
        # 5. Motif
        motif_match = re.search(r"\*Canvas Motif:\s*`([^`]+)`\*", content)
        motif = motif_match.group(1).strip() if motif_match else "Unknown Motif"
        
        # 6. Seed Hash
        seed_match = re.search(r"\*Art Seed Hash:\s*`([^`]+)`\*", content)
        seed_hash = seed_match.group(1).strip() if seed_match else ""
        
        return {
            "title": title,
            "timestamp": timestamp,
            "frame": frame,
            "stanza": stanza_lines,
            "motif": motif,
            "art_seed_hash": seed_hash,
            "filepath": str(path),
            "filename": path.name,
            "mtime": path.stat().st_mtime
        }
    except Exception:
        return None

def load_studio_gems(studio_dir: Path = STUDIO_DIR) -> List[Dict[str, Any]]:
    """Loads all gems from the studio directory, sorted by timestamp / modification time (newest first)."""
    if not studio_dir.exists():
        return []
        
    gems: List[Dict[str, Any]] = []
    for f in studio_dir.glob("art_*.md"):
        parsed = parse_gem_file(f)
        if parsed:
            gems.append(parsed)
            
    # Sort newest first
    gems.sort(key=lambda g: (g["timestamp"], g.get("mtime", 0)), reverse=True)
    return gems

# ------------------------------------------------------------------------------
# Terminal Gallery Presentation Renderer
# ------------------------------------------------------------------------------

def render_gem_card(gem: Dict[str, Any], index: int = 1, total: int = 1, width: int = 74) -> str:
    """
    Renders a micro-gem inside a beautiful bordered ANSI terminal card.
    """
    inner_w = width - 4
    lines: List[str] = []
    
    # Top border
    lines.append(f"{BOLD_PINK}╔{'═' * (width - 2)}╗{RESET}")
    
    # Header line 1: Index & Tag
    idx_info = f"🎨 KIRBY STUDIO MICRO-GEM  •  [ {index} of {total} ]"
    pad_r1 = inner_w - len(idx_info)
    lines.append(f"{BOLD_PINK}║ {BOLD_YELLOW}{idx_info}{' ' * max(0, pad_r1)} {BOLD_PINK}║{RESET}")
    
    # Header line 2: Title
    title_str = f"Title: {gem['title'].upper()}"
    if len(title_str) > inner_w:
        title_str = title_str[:inner_w - 3] + "..."
    pad_r2 = inner_w - len(title_str)
    lines.append(f"{BOLD_PINK}║ {BOLD_WHITE}{title_str}{' ' * max(0, pad_r2)} {BOLD_PINK}║{RESET}")
    
    # Header line 3: Motif & Seed
    meta_str = f"Motif: {gem['motif']}  •  Seed: {gem['art_seed_hash']}"
    if len(meta_str) > inner_w:
        meta_str = meta_str[:inner_w - 3] + "..."
    pad_r3 = inner_w - len(meta_str)
    lines.append(f"{BOLD_PINK}║ {CYAN}{meta_str}{' ' * max(0, pad_r3)} {BOLD_PINK}║{RESET}")
    
    if gem.get("timestamp"):
        ts_str = f"Painted At: {gem['timestamp']}"
        pad_ts = inner_w - len(ts_str)
        lines.append(f"{BOLD_PINK}║ {DIM}{WHITE}{ts_str}{' ' * max(0, pad_ts)} {BOLD_PINK}║{RESET}")
        
    # Divider
    lines.append(f"{BOLD_PINK}╠{'═' * (width - 2)}╣{RESET}")
    lines.append(f"{BOLD_PINK}║{' ' * (width - 2)}║{RESET}")
    
    # ASCII Art Frame
    frame_raw = gem.get("frame", "")
    for f_line in frame_raw.split("\n"):
        plain_len = len(strip_ansi(f_line))
        # Center or pad nicely
        padding_total = max(0, inner_w - plain_len)
        pad_left = padding_total // 2
        pad_right = padding_total - pad_left
        lines.append(f"{BOLD_PINK}║ {' ' * pad_left}{BOLD_CYAN}{f_line}{RESET}{' ' * pad_right} {BOLD_PINK}║{RESET}")
        
    lines.append(f"{BOLD_PINK}║{' ' * (width - 2)}║{RESET}")
    # Divider
    lines.append(f"{BOLD_PINK}╠{'═' * (width - 2)}╣{RESET}")
    
    # Stanza Header
    stanza_hdr = "📜 Stanza from the Easel:"
    pad_sh = inner_w - len(stanza_hdr)
    lines.append(f"{BOLD_PINK}║ {BOLD_GREEN}{stanza_hdr}{' ' * max(0, pad_sh)} {BOLD_PINK}║{RESET}")
    
    # Stanza Lines
    stanzas = gem.get("stanza", [])
    for idx, s_line in enumerate(stanzas):
        prefix = '  "' if idx == 0 else '   '
        suffix = '"' if idx == len(stanzas) - 1 else ''
        full_s = f"{prefix}{s_line}{suffix}"
        pad_s = inner_w - len(full_s)
        lines.append(f"{BOLD_PINK}║ {ITALIC}{WHITE}{full_s}{RESET}{' ' * max(0, pad_s)} {BOLD_PINK}║{RESET}")
        
    lines.append(f"{BOLD_PINK}║{' ' * (width - 2)}║{RESET}")
    
    # Filepath footer if known
    if gem.get("filename"):
        file_label = f"📁 {gem['filename']}"
        if len(file_label) > inner_w:
            file_label = file_label[:inner_w - 3] + "..."
        pad_fl = inner_w - len(file_label)
        lines.append(f"{BOLD_PINK}║ {DIM}{PEACH}{file_label}{RESET}{' ' * max(0, pad_fl)} {BOLD_PINK}║{RESET}")
        
    # Bottom border
    lines.append(f"{BOLD_PINK}╚{'═' * (width - 2)}╝{RESET}")
    return "\n".join(lines)

def run_gallery_browser(
    gems: Optional[List[Dict[str, Any]]] = None,
    limit: int = 10,
    show_all: bool = False,
    single_file: Optional[Path] = None,
    interactive: Optional[bool] = None
):
    """
    Interactive terminal gallery browser allowing the user to view recent gems in the terminal
    with borders and colored highlights.
    """
    if single_file:
        parsed = parse_gem_file(single_file)
        if not parsed:
            print(f"{BOLD_PINK}❌ Error:{RESET} Could not parse micro-gem from {single_file}")
            return
        gems = [parsed]
    elif gems is None:
        gems = load_studio_gems()
        
    if not gems:
        print(f"{BOLD_PINK}🎨 Kirby Studio Gallery is empty!{RESET}")
        print(f"{CYAN}Generate your first micro-gem with:{RESET} python3 kirby_studio_generator.py generate")
        return

    display_gems = gems if show_all else gems[:limit]
    total_gems = len(display_gems)
    
    # Decide whether to run interactive prompt
    is_tty = sys.stdin.isatty() if interactive is None else interactive
    
    if not is_tty:
        # Non-interactive mode (pipes, test runner, batch)
        print(f"\n{BOLD_PINK}╔══════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD_PINK}║  {BOLD_YELLOW}🌟 KIRBY STUDIO TERMINAL GALLERY BROWSER (BATCH MODE) 🌟{RESET}            {BOLD_PINK}║{RESET}")
        print(f"{BOLD_PINK}║  {CYAN}Displaying {total_gems} recent micro-gems from {STUDIO_DIR.name}/...{RESET} {' ' * max(0, 31 - len(STUDIO_DIR.name))} {BOLD_PINK}║{RESET}")
        print(f"{BOLD_PINK}╚══════════════════════════════════════════════════════════════════════╝{RESET}\n")
        
        for idx, gem in enumerate(display_gems, 1):
            print(render_gem_card(gem, index=idx, total=total_gems))
            print()
        print(f"{BOLD_GREEN}✨ Successfully rendered {total_gems} micro-gems cleanly! Poyo! (>'-')>{RESET}\n")
        return

    # Interactive TTY Mode
    curr_idx = 0
    while True:
        # Clear screen and display current gem
        print("\033[2J\033[H", end="")  # Clear ANSI screen
        curr_gem = display_gems[curr_idx]
        print(f"\n{render_gem_card(curr_gem, index=curr_idx + 1, total=total_gems)}")
        
        nav_banner = (
            f"{BOLD_CYAN}[N]{RESET} Next  "
            f"{BOLD_CYAN}[P]{RESET} Prev  "
            f"{BOLD_CYAN}[R]{RESET} Random  "
            f"{BOLD_CYAN}[A]{RESET} Print All  "
            f"{BOLD_CYAN}[Q]{RESET} Quit"
        )
        print(f"\n  {nav_banner}")
        try:
            choice = input(f"\n  {BOLD_YELLOW}Kirby Studio Navigator > {RESET}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{PINK}Goodbye, poyo! (>'-')>{RESET}\n")
            break
            
        if choice in ("q", "quit", "exit"):
            print(f"\n{PINK}Kirby waves from his easel! Poyo! (>'-')>{RESET}\n")
            break
        elif choice in ("n", "next", ""):
            curr_idx = (curr_idx + 1) % total_gems
        elif choice in ("p", "prev", "previous"):
            curr_idx = (curr_idx - 1) % total_gems
        elif choice in ("r", "random"):
            curr_idx = random.randint(0, total_gems - 1)
        elif choice in ("a", "all"):
            print("\033[2J\033[H", end="")
            for i, g in enumerate(display_gems, 1):
                print(render_gem_card(g, index=i, total=total_gems))
                print()
            input(f"{DIM}Press [Enter] to return to gallery viewer...{RESET}")
        else:
            # Try parsing a specific number
            try:
                num = int(choice)
                if 1 <= num <= total_gems:
                    curr_idx = num - 1
            except ValueError:
                pass

# ------------------------------------------------------------------------------
# CLI Dispatcher
# ------------------------------------------------------------------------------

def cli_generate(args):
    """Handler for `kirby_studio_generator.py generate`"""
    count = getattr(args, "count", 1) or 1
    save = not getattr(args, "no_save", False)
    post = not getattr(args, "no_post", False)
    title = getattr(args, "title", None)
    motif = getattr(args, "motif", None)
    seed = getattr(args, "seed", None)
    silent = getattr(args, "silent", False)
    
    generated_gems: List[Dict[str, Any]] = []
    
    for i in range(count):
        gem_seed = f"{seed}_{i}" if seed else None
        gem = generate_micro_gem(
            save=save,
            post_to_watercooler=post,
            title=title if count == 1 else None,
            motif=motif,
            seed=gem_seed
        )
        generated_gems.append(gem)
        
        if not silent:
            print(f"\n{render_gem_card(gem, index=i+1, total=count)}")
            
            # Print file and watercooler status
            if gem.get("filepath"):
                print(f"  {BOLD_GREEN}💾 Saved to:{RESET} {gem['filepath']}")
            if post:
                w_resp = gem.get("watercooler_response", {})
                if w_resp and w_resp.get("status") == "SUCCESS":
                    print(f"  {BOLD_CYAN}📡 Watercooler Dispatch:{RESET} Delivered to {w_resp.get('url')}")
                else:
                    msg = w_resp.get("message", "Offline") if w_resp else "None"
                    print(f"  {DIM}{PEACH}📡 Watercooler Dispatch:{RESET} {msg}")
            print()
            
    return generated_gems

def cli_gallery(args):
    """Handler for `kirby_studio_generator.py gallery`"""
    limit = getattr(args, "limit", 10) or 10
    show_all = getattr(args, "all", False)
    file_arg = getattr(args, "file", None)
    non_interactive = getattr(args, "non_interactive", False)
    
    single_path = Path(file_arg) if file_arg else None
    run_gallery_browser(
        limit=limit,
        show_all=show_all,
        single_file=single_path,
        interactive=False if non_interactive else None
    )

def cli_post(args):
    """Handler for `kirby_studio_generator.py post`"""
    target_url = getattr(args, "url", None)
    file_arg = getattr(args, "file", None)
    latest = getattr(args, "latest", False)
    
    if file_arg:
        p = Path(file_arg)
        gem = parse_gem_file(p)
        if not gem:
            print(f"{BOLD_PINK}❌ Error:{RESET} Could not parse {p}")
            return
    elif latest:
        gems = load_studio_gems()
        if not gems:
            print(f"{BOLD_PINK}❌ No existing gems found in {STUDIO_DIR}!{RESET}")
            return
        gem = gems[0]
    else:
        # Generate fresh gem and post
        gem = generate_micro_gem(save=True, post_to_watercooler=False)
        print(f"{BOLD_GREEN}✨ Fresh micro-gem painted for dispatch!{RESET}")
        
    print(f"{CYAN}Dispatching micro-gem \"{gem['title']}\" to Watercooler...{RESET}")
    res = dispatch_to_watercooler(gem, target_url=target_url)
    
    if res.get("status") == "SUCCESS":
        print(f"{BOLD_GREEN}✅ Success!{RESET} Delivered to {res.get('url')}")
        print(f"{DIM}Payload Message ID: {res.get('data', {}).get('message', {}).get('message_id')}{RESET}")
    else:
        print(f"{BOLD_YELLOW}⚠️ Notice:{RESET} {res.get('message')}")
        print(f"{DIM}Attempted URLs: {res.get('attempted_urls')}{RESET}")

def main():
    parser = argparse.ArgumentParser(
        prog="kirby_studio_generator.py",
        description="🎨 Kirby Studio ASCII Micro-Gem Generator & Gallery System"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # 1. generate
    p_gen = subparsers.add_parser("generate", help="Procedurally generate new ASCII micro-gem(s)")
    p_gen.add_argument("-c", "--count", type=int, default=1, help="Number of gems to generate (default: 1)")
    p_gen.add_argument("-t", "--title", type=str, default=None, help="Custom title for the gem")
    p_gen.add_argument("-m", "--motif", type=str, default=None, choices=list(MOTIF_CATALOG.keys()), help="Specify motif tag")
    p_gen.add_argument("-s", "--seed", type=str, default=None, help="Random seed for reproducible generation")
    p_gen.add_argument("--no-save", action="store_true", help="Do not write markdown file to disk")
    p_gen.add_argument("--no-post", action="store_true", help="Do not dispatch to watercooler API")
    p_gen.add_argument("--silent", action="store_true", help="Do not print terminal card")
    
    # 2. gallery
    p_gal = subparsers.add_parser("gallery", help="Open terminal gallery browser to view recent gems")
    p_gal.add_argument("-l", "--limit", type=int, default=10, help="Maximum recent gems to browse (default: 10)")
    p_gal.add_argument("-a", "--all", action="store_true", help="Browse all available gems in the studio")
    p_gal.add_argument("-f", "--file", type=str, default=None, help="View a specific markdown gem file")
    p_gal.add_argument("--non-interactive", action="store_true", help="Print gems without interactive prompt")
    
    # 3. post
    p_post = subparsers.add_parser("post", help="Dispatch a gem directly to /api/watercooler")
    p_post.add_argument("-f", "--file", type=str, default=None, help="Path to existing markdown gem to post")
    p_post.add_argument("-l", "--latest", action="store_true", help="Post the most recent existing gem in studio")
    p_post.add_argument("-u", "--url", type=str, default=None, help="Override watercooler API URL")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        cli_generate(args)
    elif args.command == "gallery":
        cli_gallery(args)
    elif args.command == "post":
        cli_post(args)
    else:
        # Default behavior if no subcommand given: generate 1 gem with full colorful preview!
        cli_generate(args)

if __name__ == "__main__":
    main()
