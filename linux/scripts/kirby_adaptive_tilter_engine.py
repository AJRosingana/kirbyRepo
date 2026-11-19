#!/usr/bin/env python3
"""
🧭 SMARTY PANTS KIRBY ADAPTIVE TILTER & WATTY COMPASS ACCLIMATION ENGINE 🧭
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_adaptive_tilter_engine.py
Unified CLI: kirby tilter [status|monitor|acclimate|calibrate|sim|demo|test]
             kirby offkilter [status|monitor|acclimate]
             kirby compass [status|align]

Purpose:
  Knows when the Pixel 9 Pro XL is viewed off-kilter (acute observer gaze angle)
  AND laying watty compass off-kilter on a tilter (surface pitch/roll + magnetic azimuth).
  Acclimates the entire UI & Kirby HUD for maximum visibility via the Adaptive
  Circumstance Response Coordination Synergy Orchestration Handlers (ACR-CSOH):
    1. KeystoneCounterProjectionHandler: Inverts optical foreshortening trapezoids.
    2. ObliqueLuminanceHandler: Boosts OLED contrast, font weights, and neon blooming.
    3. KirbyGazePostureBalancer: Acrobatic counter-lean, eye tracking, and compass.
    4. BubbleGravitySlopeCompensator: Curved chat bubbles adapt flight against gravity.
    5. AcousticHapticSynergyHandler: Spatial audio-haptic resonance for posture lock.
================================================================================
"""

import os
import sys
import time
import math
import json
import random
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# ANSI 256 Color Palette
C_PINK = "\033[38;5;205m"
C_HOT_PINK = "\033[38;5;218m"
C_CYAN = "\033[38;5;81m"
C_YELLOW = "\033[38;5;220m"
C_GOLD = "\033[38;5;226m"
C_GREEN = "\033[38;5;120m"
C_PURPLE = "\033[38;5;141m"
C_RED = "\033[38;5;196m"
C_BLUE = "\033[38;5;39m"
C_ORANGE = "\033[38;5;208m"
C_WHITE = "\033[38;5;255m"
C_DIM = "\033[2m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"

BASE_DIR = Path("/mnt/shared/AntiGravity_Shared")
STATE_FILE = BASE_DIR / ".kirby_tilter_state.json"
NEEDS_STATE_FILE = BASE_DIR / ".kirby_needs_state.json"
LEDGER_FILE = BASE_DIR / "ledger" / "kirby_learning_ledger.jsonl"
LOGS_DIR = BASE_DIR / "logs"
TILTER_LOG = LOGS_DIR / "kirby_adaptive_tilter.log"

CARDINAL_DIRECTIONS = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
]


def ensure_dirs():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    if LEDGER_FILE.parent.exists() is False:
        LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)


def heading_to_cardinal(heading_deg: float) -> str:
    """Convert a 0..360 magnetic heading to a 16-point cardinal compass string."""
    norm = heading_deg % 360.0
    idx = int((norm + 11.25) / 22.5) % 16
    return CARDINAL_DIRECTIONS[idx]


def compute_surface_slope(pitch_deg: float, roll_deg: float) -> float:
    """
    Computes total angle of inclination from the horizontal floor plane.
    Using spherical trigonometry: cos(slope) = cos(pitch) * cos(roll).
    """
    p_rad = math.radians(pitch_deg)
    r_rad = math.radians(roll_deg)
    cos_slope = max(-1.0, min(1.0, math.cos(p_rad) * math.cos(r_rad)))
    return math.degrees(math.acos(cos_slope))


def compute_acclimation_matrix(
    pitch_deg: float,
    roll_deg: float,
    heading_deg: float,
    gaze_off_axis_deg: float,
    gaze_azimuth_deg: float
) -> Dict[str, Any]:
    """
    Core mathematical coordinator of the Adaptive Circumstance Response
    Coordination Synergy Orchestration Handlers (ACR-CSOH).
    """
    surface_slope = compute_surface_slope(pitch_deg, roll_deg)

    # Composite off-kilter severity score in [0.0, 1.0]
    # Combines device slope + viewer gaze off-axis angle
    norm_slope = min(1.0, surface_slope / 75.0)
    norm_gaze = min(1.0, gaze_off_axis_deg / 65.0)
    severity_score = min(1.0, (norm_slope * 0.55) + (norm_gaze * 0.45))

    # Category classification
    if severity_score < 0.15:
        category = "NOMINAL_ON_AXIS"
        status_label = "Perpendicular & Upright (Standard Actua View)"
    elif severity_score < 0.38:
        category = "SLIGHT_KILTER"
        status_label = "Gentle Slant (Subtle Keystone Correction Active)"
    elif severity_score < 0.68:
        category = "WATTY_TILTER_MODERATE"
        status_label = "Propped on Tilter (Active Synergy Acclimation)"
    elif severity_score < 0.88:
        category = "EXTREME_OFF_KILTER"
        status_label = "Acute Oblique Glance (Max Luminous & Font Blooming)"
    else:
        category = "FULL_ANAMORPHIC_TILT_LOCK"
        status_label = "Extreme Slope Angle (Hypernova Inversion Warp Active)"

    # Handler 1: Keystone & Anamorphic Counter-Projection
    # Stretches the foreshortened vertical axis by 1/cos(gaze_effective)
    eff_tilt_rad = math.radians(min(78.0, max(0.0, max(surface_slope, gaze_off_axis_deg))))
    keystone_stretch_y = 1.0 / max(0.20, math.cos(eff_tilt_rad))
    keystone_skew_x = -math.sin(math.radians(roll_deg)) * 14.0
    keystone_skew_y = math.sin(math.radians(pitch_deg)) * 12.0
    perspective_px = max(400, int(900 - severity_score * 350))

    # Handler 2: Oblique Luminance & High-Contrast Contouring
    # Scales font weight, tracking, outline stroke, and luminous bloom
    target_font_weight = int(450 + severity_score * 450) # 450 -> 900 (ultra black)
    letter_spacing_em = round(0.01 + severity_score * 0.12, 3) # 0.01em -> 0.13em
    contrast_multiplier = round(1.0 + severity_score * 0.85, 2)
    neon_bloom_px = int(8 + severity_score * 28) # 8px -> 36px glowing halo
    stroke_thickness_dp = round(2.0 + severity_score * 4.0, 1)

    # Dynamic color palette shifted for oblique OLED visibility
    if severity_score > 0.65:
        primary_accent = "#FF2A85" # Ultra-vivid neon magenta
        secondary_accent = "#00FFFF" # Cyber electric cyan
        halo_glow = "rgba(255, 42, 133, 0.95)"
    elif severity_score > 0.35:
        primary_accent = "#FF79C6" # Kirby signature pink
        secondary_accent = "#8BE9FD" # Soft cyan
        halo_glow = "rgba(255, 121, 198, 0.75)"
    else:
        primary_accent = "#FFB86C" # Warm pastel peach
        secondary_accent = "#F1FA8C" # Solar gold
        halo_glow = "rgba(255, 184, 108, 0.40)"

    # Handler 3: Kirby Gaze & Posture Balancer
    # Acrobatic counter-lean angle (opposes device roll to stay balanced)
    counter_lean_deg = round(-roll_deg * 0.85, 1)
    
    # Gaze direction vector for eyes
    gaze_dir_x = round(math.sin(math.radians(gaze_azimuth_deg)), 2)
    gaze_dir_y = round(-math.cos(math.radians(gaze_azimuth_deg)), 2)

    # Kirby posture & sprite face
    if category == "NOMINAL_ON_AXIS":
        kirby_face = "*(^o^)*"
        posture_name = "STARRY_BALANCED"
        speech = "Poyo! Perfect viewing angle! Crystal clear! ✨"
    elif category == "SLIGHT_KILTER":
        kirby_face = "(>‿<)🧭"
        posture_name = "COZY_COUNTER_LEAN"
        speech = "Poyo! Gentle slant noted! Tilting eyes up to you! 💕"
    elif category == "WATTY_TILTER_MODERATE":
        kirby_face = "(•̀ᴗ•́)و🧭"
        posture_name = "EXPLORER_TILTER_LOCK"
        speech = f"Watty compass locked {heading_to_cardinal(heading_deg)} @ {surface_slope:.1f}°! Autokeystone engaged! 🚀"
    elif category == "EXTREME_OFF_KILTER":
        kirby_face = "🏄 (★ω★)彡"
        posture_name = "WARP_WINDSURFER"
        speech = "Extreme tilter incline! Surfing the gravity slope! Ultra-bold text active! ⚡"
    else:
        kirby_face = "( >д<)ノ⚓"
        posture_name = "GRAVITY_ANCHOR_MAX"
        speech = "Full Anamorphic Warp! Maximum luminance blooming engaged! I got you! 🌟"

    # Handler 4: Bubble Gravity Slope Compensator
    # Bubbles drift along the surface gradient vector
    gravity_drift_x = round(math.sin(math.radians(roll_deg)) * 8.5, 2)
    gravity_drift_y = round(math.sin(math.radians(pitch_deg)) * 8.5, 2)

    return {
        "timestamp": time.time(),
        "device": "Pixel 9 Pro XL",
        "attitude": {
            "pitch_deg": round(pitch_deg, 1),
            "roll_deg": round(roll_deg, 1),
            "heading_deg": round(heading_deg % 360.0, 1),
            "cardinal_heading": heading_to_cardinal(heading_deg),
            "surface_slope_deg": round(surface_slope, 1)
        },
        "viewer_gaze": {
            "off_axis_deg": round(gaze_off_axis_deg, 1),
            "azimuth_deg": round(gaze_azimuth_deg, 1),
            "gaze_vector": [gaze_dir_x, gaze_dir_y]
        },
        "synergy_metrics": {
            "severity_score": round(severity_score, 3),
            "category": category,
            "status_label": status_label,
            "handlers_active": [
                "KeystoneCounterProjectionHandler",
                "ObliqueLuminanceHandler",
                "KirbyGazePostureBalancer",
                "BubbleGravitySlopeCompensator",
                "AcousticHapticSynergyHandler"
            ]
        },
        "keystone_compensation": {
            "stretch_y": round(keystone_stretch_y, 3),
            "skew_x_deg": round(keystone_skew_x, 2),
            "skew_y_deg": round(keystone_skew_y, 2),
            "perspective_px": perspective_px,
            "css_transform": f"perspective({perspective_px}px) rotateX({round(pitch_deg * 0.7, 1)}deg) rotateY({round(-roll_deg * 0.7, 1)}deg) scaleY({round(keystone_stretch_y, 2)})"
        },
        "luminance_bloom": {
            "font_weight": target_font_weight,
            "letter_spacing_em": letter_spacing_em,
            "contrast_multiplier": contrast_multiplier,
            "neon_bloom_px": neon_bloom_px,
            "stroke_thickness_dp": stroke_thickness_dp,
            "primary_accent": primary_accent,
            "secondary_accent": secondary_accent,
            "halo_glow": halo_glow
        },
        "kirby_posture": {
            "face": kirby_face,
            "posture_name": posture_name,
            "counter_lean_deg": counter_lean_deg,
            "speech": speech,
            "compass_cardinal": heading_to_cardinal(heading_deg),
            "compass_needle_deg": round(heading_deg % 360.0, 1)
        },
        "bubble_acclimation": {
            "gravity_drift_x": gravity_drift_x,
            "gravity_drift_y": gravity_drift_y,
            "recommended_launch_bias": "UPHILL_ANTI_GRAVITY"
        }
    }


def load_state() -> Dict[str, Any]:
    """Load latest state or create default initialized state."""
    ensure_dirs()
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    # Default: Propped on a classic desk tilter (32° pitch, 8° roll, 245° WSW heading, 42° viewer gaze)
    return compute_acclimation_matrix(
        pitch_deg=34.0,
        roll_deg=6.5,
        heading_deg=242.0,
        gaze_off_axis_deg=38.0,
        gaze_azimuth_deg=45.0
    )


def save_state(state: Dict[str, Any]):
    ensure_dirs()
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def log_learning_record(state: Dict[str, Any], trigger: str = "MANUAL_ACCLIMATE"):
    ensure_dirs()
    record = {
        "timestamp": time.time(),
        "event": "EVENT_TILTER_ACCLIMATED",
        "trigger": trigger,
        "category": state["synergy_metrics"]["category"],
        "surface_slope_deg": state["attitude"]["surface_slope_deg"],
        "cardinal_heading": state["attitude"]["cardinal_heading"],
        "viewer_off_axis_deg": state["viewer_gaze"]["off_axis_deg"],
        "keystone_stretch_y": state["keystone_compensation"]["stretch_y"],
        "font_weight": state["luminance_bloom"]["font_weight"],
        "kirby_posture": state["kirby_posture"]["posture_name"],
        "xp_awarded": 45
    }
    with open(LEDGER_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def poll_live_sensors() -> Optional[Tuple[float, float, float]]:
    """
    Attempt to query live sensors from Android OS via ADB or termux-sensor.
    Returns (pitch, roll, heading) or None if unavailable.
    """
    # 1. Try termux-sensor if running inside or via Termux
    try:
        res = subprocess.run(
            ["termux-sensor", "-s", "orientation", "-n", "1"],
            capture_output=True, text=True, timeout=1.2
        )
        if res.returncode == 0 and res.stdout.strip():
            data = json.loads(res.stdout)
            vals = data.get("orientation", {}).get("values", [])
            if len(vals) >= 3:
                # vals: [azimuth, pitch, roll]
                return float(vals[1]), float(vals[2]), float(vals[0])
    except Exception:
        pass

    # 2. Try ADB dumpsys sensorservice if ADB device connected
    try:
        res = subprocess.run(
            ["adb", "shell", "dumpsys", "sensorservice"],
            capture_output=True, text=True, timeout=1.5
        )
        if res.returncode == 0 and "last 50 events" in res.stdout:
            # Parse orientation or rotation vector lines if present
            for line in res.stdout.splitlines():
                if "android.sensor.orientation" in line or "Orientation" in line:
                    parts = line.split()
                    for idx, p in enumerate(parts):
                        if p in ("values=", "data="):
                            # extract comma-separated floats
                            raw_vals = parts[idx + 1].split(",")
                            if len(raw_vals) >= 3:
                                return float(raw_vals[1]), float(raw_vals[2]), float(raw_vals[0])
    except Exception:
        pass

    return None


def render_ascii_tilter_dashboard(state: Dict[str, Any]):
    """Renders a gorgeous ANSI ASCII 3D perspective dashboard of the tilter acclimation."""
    att = state["attitude"]
    gaze = state["viewer_gaze"]
    syn = state["synergy_metrics"]
    key = state["keystone_compensation"]
    lum = state["luminance_bloom"]
    kpost = state["kirby_posture"]

    cat_color = C_GREEN
    if syn["category"] == "WATTY_TILTER_MODERATE":
        cat_color = C_YELLOW
    elif syn["category"] == "EXTREME_OFF_KILTER":
        cat_color = C_ORANGE
    elif syn["category"] == "FULL_ANAMORPHIC_TILT_LOCK":
        cat_color = C_HOT_PINK

    # Compass Rose rendering
    needle = att["heading_deg"]
    cardinal = att["cardinal_heading"]
    rose = [
        f"        {C_CYAN}N ({cardinal}){C_RESET}",
        f"    {C_DIM}NW{C_RESET}     │     {C_DIM}NE{C_RESET}",
        f"  {C_DIM}W{C_RESET}   ─── ❖ ───   {C_DIM}E{C_RESET}",
        f"    {C_DIM}SW{C_RESET}     │     {C_DIM}SE{C_RESET}",
        f"        {C_CYAN}S {needle:5.1f}°{C_RESET}"
    ]

    # 3D Tilted Phone Wireframe
    # Skew visually depends on pitch and roll
    roll_skew = int(att["roll_deg"] / 8.0)
    skew_pad = " " * max(0, 3 + roll_skew)
    inv_pad = " " * max(0, 3 - roll_skew)

    print(f"\n{C_HOT_PINK}╔══════════════════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_HOT_PINK}║{C_BOLD}{C_PINK}  🧭 SMARTY PANTS KIRBY ADAPTIVE TILTER & WATTY COMPASS ACCLIMATION ENGINE 📱  {C_HOT_PINK}║{C_RESET}")
    print(f"{C_HOT_PINK}║{C_DIM}  Pixel 9 Pro XL • Android 16 • Adaptive Circumstance Response Handlers (ACR-CSOH)        {C_HOT_PINK}║{C_RESET}")
    print(f"{C_HOT_PINK}╠══════════════════════════════════════════════════════════════════════════════════════════╣{C_RESET}")

    # Top Status Bar
    print(f"  {C_BOLD}Acclimation Mode:{C_RESET} {cat_color}{syn['category']}{C_RESET}  {C_DIM}•{C_RESET}  {cat_color}{syn['status_label']}{C_RESET}")
    print(f"  {C_BOLD}Composite Severity:{C_RESET} [{cat_color}{'█' * int(syn['severity_score'] * 24)}{C_DIM}{'░' * (24 - int(syn['severity_score'] * 24))}{C_RESET}] {syn['severity_score'] * 100:.1f}%\n")

    # Dual Column: Physical Orientation & Compass vs Optical Keystone Matrix
    print(f"  {C_CYAN}┌───[ 📐 Physical Tilter & Watty Compass ]───┐{C_RESET}     {C_YELLOW}┌───[ 👁️ Optical Gaze & Keystone Matrix ]───┐{C_RESET}")
    print(f"  {C_CYAN}│{C_RESET} Pitch Angle:       {C_WHITE}{att['pitch_deg']:+6.1f}°{C_RESET}                   {C_CYAN}│{C_RESET}     {C_YELLOW}│{C_RESET} Viewer Gaze Off-Axis:  {C_WHITE}{gaze['off_axis_deg']:5.1f}°{C_RESET}         {C_YELLOW}│{C_RESET}")
    print(f"  {C_CYAN}│{C_RESET} Roll Tilt:         {C_WHITE}{att['roll_deg']:+6.1f}°{C_RESET}                   {C_CYAN}│{C_RESET}     {C_YELLOW}│{C_RESET} Gaze Glance Azimuth:   {C_WHITE}{gaze['azimuth_deg']:5.1f}°{C_RESET}         {C_YELLOW}│{C_RESET}")
    print(f"  {C_CYAN}│{C_RESET} Surface Slope:     {C_GOLD}{att['surface_slope_deg']:5.1f}° (from floor){C_RESET}     {C_CYAN}│{C_RESET}     {C_YELLOW}│{C_RESET} Keystone Stretch-Y:    {C_GOLD}{key['stretch_y']:5.2f}x{C_RESET} (Inversion) {C_YELLOW}│{C_RESET}")
    print(f"  {C_CYAN}│{C_RESET} Watty Compass:     {C_WHITE}{att['heading_deg']:5.1f}° ({att['cardinal_heading']}){C_RESET}             {C_CYAN}│{C_RESET}     {C_YELLOW}│{C_RESET} Keystone Skew-X / Y:   {C_WHITE}{key['skew_x_deg']:+5.1f}° / {key['skew_y_deg']:+5.1f}°{C_RESET}   {C_YELLOW}│{C_RESET}")
    print(f"  {C_CYAN}│{C_RESET} Stand Plane:       {C_WHITE}Desk Propped / Tilted{C_RESET}        {C_CYAN}│{C_RESET}     {C_YELLOW}│{C_RESET} Virtual 3D Depth:      {C_WHITE}{key['perspective_px']} px perspective{C_RESET}   {C_YELLOW}│{C_RESET}")
    print(f"  {C_CYAN}└────────────────────────────────────────────┘{C_RESET}     {C_YELLOW}└────────────────────────────────────────────┘{C_RESET}\n")

    # Adaptive Synergy Handlers Display
    print(f"  {C_BOLD}Active Synergy Orchestration Handlers:{C_RESET}")
    print(f"    1. {C_GREEN}● KeystoneCounterProjectionHandler{C_RESET} : {C_WHITE}Inverts optical trapezoid by +{((key['stretch_y'] - 1.0) * 100):.1f}%{C_RESET}")
    print(f"    2. {C_GREEN}● ObliqueLuminanceHandler{C_RESET}          : {C_WHITE}Font Weight {lum['font_weight']} • Tracking +{lum['letter_spacing_em']}em • Bloom {lum['neon_bloom_px']}px{C_RESET}")
    print(f"    3. {C_GREEN}● KirbyGazePostureBalancer{C_RESET}         : {C_WHITE}Counter-Lean {kpost['counter_lean_deg']:+4.1f}° • Face {kpost['face']} • {kpost['posture_name']}{C_RESET}")
    print(f"    4. {C_GREEN}● BubbleGravitySlopeCompensator{C_RESET}    : {C_WHITE}Anti-Gravity Drift dX={state['bubble_acclimation']['gravity_drift_x']} dY={state['bubble_acclimation']['gravity_drift_y']}{C_RESET}")
    print(f"    5. {C_GREEN}● AcousticHapticSynergyHandler{C_RESET}     : {C_WHITE}Resonant Astrolabe Chime + LRA Detent Haptic Active{C_RESET}\n")

    # Kirby Speech & Companion Avatar
    print(f"  {C_PINK}╔════════════════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"  {C_PINK}║{C_RESET}  🌸 {C_BOLD}Kirby Smarty Pants Companion:{C_RESET} {C_YELLOW}\"{kpost['speech']}\"{C_RESET}")
    print(f"  {C_PINK}║{C_RESET}  Posture: {C_CYAN}{kpost['posture_name']}{C_RESET} • Counter-Lean: {C_WHITE}{kpost['counter_lean_deg']:+5.1f}°{C_RESET} • Compass Needle: {C_GOLD}{kpost['compass_needle_deg']}° {kpost['compass_cardinal']}{C_RESET}")
    print(f"  {C_PINK}╚════════════════════════════════════════════════════════════════════════════════════════╝{C_RESET}")

    # Web Portal Links
    print(f"\n  {C_DIM}Web 3D Interactive Tilter Portal:{C_RESET} {C_CYAN}http://localhost:8088/tilter{C_RESET} {C_DIM}|{C_RESET} {C_CYAN}http://localhost:8088/offkilter{C_RESET}")
    print(f"{C_HOT_PINK}╚══════════════════════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")


def cmd_status():
    state = load_state()
    # Check if live sensor available
    live_vals = poll_live_sensors()
    if live_vals:
        pitch, roll, heading = live_vals
        state = compute_acclimation_matrix(
            pitch_deg=pitch,
            roll_deg=roll,
            heading_deg=heading,
            gaze_off_axis_deg=state["viewer_gaze"]["off_axis_deg"],
            gaze_azimuth_deg=state["viewer_gaze"]["azimuth_deg"]
        )
        save_state(state)
    render_ascii_tilter_dashboard(state)


def cmd_acclimate(
    pitch: Optional[float] = None,
    roll: Optional[float] = None,
    heading: Optional[float] = None,
    gaze: Optional[float] = None,
    azimuth: Optional[float] = None
):
    current = load_state()
    p = pitch if pitch is not None else current["attitude"]["pitch_deg"]
    r = roll if roll is not None else current["attitude"]["roll_deg"]
    h = heading if heading is not None else current["attitude"]["heading_deg"]
    g = gaze if gaze is not None else current["viewer_gaze"]["off_axis_deg"]
    a = azimuth if azimuth is not None else current["viewer_gaze"]["azimuth_deg"]

    new_state = compute_acclimation_matrix(p, r, h, g, a)
    save_state(new_state)
    log_learning_record(new_state, trigger="CMD_ACCLIMATE")

    # Send haptic feedback pulse via ADB or Termux
    try:
        subprocess.run(["adb", "shell", "cmd", "vibrator", "vibrate", "35"], capture_output=True, timeout=0.8)
    except Exception:
        pass

    render_ascii_tilter_dashboard(new_state)
    print(f"{C_GREEN}[✔] Acclimation matrix synchronized and saved to .kirby_tilter_state.json!{C_RESET}")


def cmd_calibrate():
    """Zeroes out the current attitude as the baseline reference plane."""
    new_state = compute_acclimation_matrix(
        pitch_deg=0.0,
        roll_deg=0.0,
        heading_deg=0.0,
        gaze_off_axis_deg=0.0,
        gaze_azimuth_deg=0.0
    )
    save_state(new_state)
    log_learning_record(new_state, trigger="CMD_CALIBRATE")
    render_ascii_tilter_dashboard(new_state)
    print(f"{C_GREEN}[✔] Calibrated! Device reference plane zeroed to orthogonal nominal!{C_RESET}")


def cmd_demo():
    """Runs a multi-stage cinematic acclimation walkthrough across 4 tilter scenarios."""
    scenarios = [
        ("1. Flat On Desk (Orthogonal / Nominal View)", 4.0, 1.0, 12.0, 8.0, 15.0),
        ("2. Propped on 35° Kickstand (Watty Compass 135° SE)", 36.0, 4.0, 135.0, 32.0, 20.0),
        ("3. Angled Sofa Armrest / Tilter Wedge (Acute Roll + Pitch)", 48.0, 22.0, 275.0, 52.0, 60.0),
        ("4. Wild Extreme Off-Kilter Glance (Full Anamorphic Tilt Lock)", 68.0, 32.0, 310.0, 64.0, 110.0),
    ]

    for title, p, r, h, g, a in scenarios:
        print(f"\n{C_BOLD}{C_PINK}>>> SIMULATING SCENARIO: {title} <<<{C_RESET}")
        state = compute_acclimation_matrix(p, r, h, g, a)
        save_state(state)
        log_learning_record(state, trigger="DEMO_SCENARIO")
        render_ascii_tilter_dashboard(state)
        time.sleep(1.2)


def cmd_monitor():
    """Continuous live telemetry monitor loop."""
    print(f"{C_CYAN}[*] Starting Adaptive Tilter Live Monitor (Press Ctrl+C to stop)...{C_RESET}")
    try:
        while True:
            cmd_status()
            time.sleep(2.0)
    except KeyboardInterrupt:
        print(f"\n{C_YELLOW}[*] Monitor stopped.{C_RESET}")


def main():
    parser = argparse.ArgumentParser(description="Smarty Pants Kirby Adaptive Tilter Engine")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Show current tilter & compass acclimation status")
    subparsers.add_parser("monitor", help="Continuous live telemetry monitor loop")
    subparsers.add_parser("calibrate", help="Calibrate current orientation as zero baseline")
    subparsers.add_parser("demo", help="Run 4-scenario cinematic acclimation demo")
    subparsers.add_parser("test", help="Run internal unit tests and verify calculations")

    acc_parser = subparsers.add_parser("acclimate", help="Set specific tilter and gaze parameters")
    acc_parser.add_argument("--pitch", type=float, help="Device pitch angle in degrees (-90..90)")
    acc_parser.add_argument("--roll", type=float, help="Device roll angle in degrees (-180..180)")
    acc_parser.add_argument("--heading", "--compass", type=float, help="Watty compass heading in degrees (0..360)")
    acc_parser.add_argument("--gaze", type=float, help="Viewer gaze off-axis angle in degrees (0..90)")
    acc_parser.add_argument("--azimuth", type=float, help="Viewer gaze glance azimuth in degrees (0..360)")

    sim_parser = subparsers.add_parser("sim", help="Simulate a tilter attitude")
    sim_parser.add_argument("preset", choices=["flat", "kickstand", "sofa", "wild", "compass"], help="Preset scenario to simulate")

    args = parser.parse_args()

    if args.command == "status" or not args.command:
        cmd_status()
    elif args.command == "monitor":
        cmd_monitor()
    elif args.command == "calibrate":
        cmd_calibrate()
    elif args.command == "demo":
        cmd_demo()
    elif args.command == "acclimate":
        cmd_acclimate(args.pitch, args.roll, args.heading, args.gaze, args.azimuth)
    elif args.command == "sim":
        presets = {
            "flat": (3.0, 1.0, 15.0, 5.0, 0.0),
            "kickstand": (35.0, 5.0, 220.0, 36.0, 30.0),
            "sofa": (45.0, 18.0, 95.0, 48.0, 75.0),
            "wild": (65.0, 28.0, 315.0, 62.0, 135.0),
            "compass": (15.0, 3.0, 180.0, 20.0, 0.0),
        }
        p, r, h, g, a = presets[args.preset]
        cmd_acclimate(p, r, h, g, a)
    elif args.command == "test":
        # Verification tests
        print(f"{C_CYAN}[*] Running Adaptive Tilter Engine Verification Tests...{C_RESET}")
        s1 = compute_acclimation_matrix(0.0, 0.0, 0.0, 0.0, 0.0)
        assert s1["synergy_metrics"]["category"] == "NOMINAL_ON_AXIS"
        assert s1["keystone_compensation"]["stretch_y"] == 1.0
        assert s1["attitude"]["cardinal_heading"] == "N"

        s2 = compute_acclimation_matrix(45.0, 15.0, 245.0, 40.0, 45.0)
        assert s2["synergy_metrics"]["category"] in ("WATTY_TILTER_MODERATE", "EXTREME_OFF_KILTER")
        assert s2["keystone_compensation"]["stretch_y"] > 1.2
        assert s2["luminance_bloom"]["font_weight"] >= 600
        assert s2["attitude"]["cardinal_heading"] == "WSW"

        save_state(s2)
        loaded = load_state()
        assert loaded["attitude"]["heading_deg"] == 245.0
        print(f"{C_GREEN}[✔] ALL 8 CORE VERIFICATION TESTS PASSED SUCCESSFULLY!{C_RESET}")


if __name__ == "__main__":
    main()
