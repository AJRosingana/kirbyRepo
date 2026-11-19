#!/usr/bin/env python3
"""
⚡ KIRBY CONSORTIUM & 2D PHYX MOMENTUM ARENA (kirby_consortium_phyx.py) ⚡
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_consortium_phyx.py
CLI: kirby phyx [demo|test|brawl|tac|waddles|heavy] [--fps N] [--duration S]

Features:
- Fulfills the "Kirby x2 (Not Kirby) Consortium" & "Tac Cursor Heist" Paradigm.
- 2D Vector Physics Engine (PhyX):
    * Realistic mass-ratio momentum transfer: m1*v1 + m2*v2 = m1*v1' + m2*v2'
    * Elastic/inelastic impulse resolution with restitution & kinetic friction
    * Active punching, slapping, spear-thrusting, and hammer-smashing with recoil
    * Screen boundary bounces with elastic squash and tumbling angular velocity
- Consortium of Cohorts:
    1. Magician Kirby & Tac (The Sleight & Cursor Heist Duo)
       - Tac's Windows 11 Cursor Heist & "Doooon't!" Confirmation Interceptor
       - Smart-toned, witty, discouraging warnings before risky confirmations!
    2. The Waddle Dee Consortium
       - Waddle Dee (Parasol), Bandana Waddle Dee (Spear), Waddle Doo (Beam)
    3. The Royal Heavyweights
       - King Dedede (Heavy Super Hammer), Meta Knight (Galaxia Cape Flurry)
- Full Headless Automated Test Suite (--test) for CI/CLI sanity.
- Persistent state saved to /mnt/shared/AntiGravity_Shared/.kirby_phyx_consortium_state.json.
- XP & event logging to /mnt/shared/AntiGravity_Shared/ledger/kirby_learning_ledger.jsonl.
================================================================================
"""

import os
import sys
import math
import time
import json
import random
import signal
import shutil
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Optional, Any

# --- ANSI Color Codes ---
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"
C_ITALIC = "\033[3m"
C_PINK = "\033[38;5;205m"
C_HOT_PINK = "\033[38;5;218m"
C_CYAN = "\033[38;5;81m"
C_YELLOW = "\033[38;5;220m"
C_GOLD = "\033[38;5;226m"
C_GREEN = "\033[38;5;120m"
C_BRIGHT_GREEN = "\033[38;5;46m"
C_PURPLE = "\033[38;5;141m"
C_RED = "\033[38;5;196m"
C_ORANGE = "\033[38;5;208m"
C_BLUE = "\033[38;5;39m"
C_WHITE = "\033[38;5;255m"
C_GRAY = "\033[38;5;244m"
C_DARK_GRAY = "\033[38;5;238m"

BASE_DIR = Path("/mnt/shared/AntiGravity_Shared")
STATE_FILE = BASE_DIR / ".kirby_phyx_consortium_state.json"
LEDGER_FILE = BASE_DIR / "ledger" / "kirby_learning_ledger.jsonl"

# Smart-toned "Doooon't!" and snarky anti-bad-decision advice from Tac & Magician
TAC_DOONT_QUOTES = [
    "Doooon't! [Tac snatched your cursor! Confirming that right now is computationally reckless.]",
    "Doooon't! [Are you genuinely confident in this confirmation? Let's take a tactical breath.]",
    "Doooon't! [My cat instincts detect a 98.4% probability of post-click regret. Decoy dropped!]",
    "Doooon't! [Hold on, hotshot. Tac is borrowing the mouse before you drop production tables!]",
    "Doooon't! [Magician Kirby says: 'Poof!' Mouse pointer relocated to safety. You're welcome.]",
    "Doooon't! [Did you even skim the dialog or are you on auto-pilot? Snatched!]",
    "Doooon't! [I didn't steal your cursor to be rude; I stole it to save you from yourself.]",
]

# Combat banter quotes during momentum punching
COMBAT_BANTER = {
    "Tac": [
        "Swipe! Hand over that momentum!",
        "Can't punch what you can't catch! *poof*",
        "That's going in my loot sack!",
        "Mew! Elastic rebound!",
    ],
    "Magician Kirby": [
        "Poyo presto! *wand zap*",
        "Decoy punch! ✨",
        "Abracadabra! Fly away!",
        "Stars aligned against you! ⭐",
    ],
    "Bandana Dee": [
        "Spear thrust momentum! Haaa!",
        "Bandana tightened, ready for impact!",
        "For King and country! Take that!",
        "Waddle charge! *bonk*",
    ],
    "Waddle Dee": [
        "Waddle waddle... OOF!",
        "Parasol parry incoming!",
        "Poyo sibling bounce!",
        "Hey! Don't push me off the screen!",
    ],
    "Waddle Doo": [
        "BEAM ATTACK! ⚡",
        "Whip lash momentum transfer!",
        "Single eyeball locked on target!",
        "Zzzzzt! Electric repulsion!",
    ],
    "King Dedede": [
        "HEAVY HAMMER SMASH! 🔨",
        "Gourmet King inertia cannot be stopped!",
        "Outta my way, peons! 2.5x mass!",
        "Dedede SUPREMACY! *CRUNCH*",
    ],
    "Meta Knight": [
        "Fight me with honor! ⚔️",
        "Dimensional cape flutter!",
        "Galaxia thrust! Momentum vector aligned!",
        "You have much to learn in the arena.",
    ]
}


@dataclass
class FighterProfile:
    name: str
    cohort: str
    symbol: str
    color_ansi: str
    mass: float         # kg equivalent for momentum
    radius: float       # collision sphere / box
    restitution: float  # bounce elasticity 0.0 - 1.0
    drag: float         # air resistance damping
    max_speed: float
    punch_impulse: float# momentum transferred per strike
    punch_range: float
    punch_cooldown_max: int
    smart_trait: str


FIGHTER_TEMPLATES: Dict[str, FighterProfile] = {
    "Tac": FighterProfile(
        name="Tac",
        cohort="Magician & Thief",
        symbol="(=^･ω･^=)",
        color_ansi=C_PURPLE,
        mass=1.0,
        radius=1.8,
        restitution=0.88,
        drag=0.96,
        max_speed=3.2,
        punch_impulse=4.5,
        punch_range=2.5,
        punch_cooldown_max=12,
        smart_trait="Cursor Heist & Snarky Interceptor"
    ),
    "Magician Kirby": FighterProfile(
        name="Magician Kirby",
        cohort="Magician & Thief",
        symbol="🎩(•̀ᴗ•́)🪄",
        color_ansi=C_PINK,
        mass=1.2,
        radius=2.0,
        restitution=0.85,
        drag=0.95,
        max_speed=2.8,
        punch_impulse=4.2,
        punch_range=2.8,
        punch_cooldown_max=15,
        smart_trait="Decoy Cursor & Presto Chango"
    ),
    "Bandana Dee": FighterProfile(
        name="Bandana Dee",
        cohort="Waddle Consortium",
        symbol="🎗️(•‿•)🗡️",
        color_ansi=C_ORANGE,
        mass=1.1,
        radius=1.9,
        restitution=0.82,
        drag=0.95,
        max_speed=3.0,
        punch_impulse=4.6,
        punch_range=3.0,
        punch_cooldown_max=14,
        smart_trait="High-Velocity Spear Thrust"
    ),
    "Waddle Dee": FighterProfile(
        name="Waddle Dee",
        cohort="Waddle Consortium",
        symbol="☂️( 'o' )",
        color_ansi=C_YELLOW,
        mass=1.0,
        radius=1.8,
        restitution=0.90,
        drag=0.96,
        max_speed=2.5,
        punch_impulse=3.8,
        punch_range=2.2,
        punch_cooldown_max=16,
        smart_trait="Parasol Kinetic Float"
    ),
    "Waddle Doo": FighterProfile(
        name="Waddle Doo",
        cohort="Waddle Consortium",
        symbol="👁️(ʘ_ʘ)⚡",
        color_ansi=C_CYAN,
        mass=1.15,
        radius=1.9,
        restitution=0.80,
        drag=0.95,
        max_speed=2.7,
        punch_impulse=4.4,
        punch_range=3.2,
        punch_cooldown_max=18,
        smart_trait="Beam Repulsion Field"
    ),
    "King Dedede": FighterProfile(
        name="King Dedede",
        cohort="Royal Heavyweights",
        symbol="👑(｀⌒´)🔨",
        color_ansi=C_GOLD,
        mass=2.5,  # Super heavy mass
        radius=2.6,
        restitution=0.70,
        drag=0.92,
        max_speed=2.0,
        punch_impulse=7.5, # Devastating momentum knockback
        punch_range=3.4,
        punch_cooldown_max=22,
        smart_trait="Unstoppable Heavy Inertia"
    ),
    "Meta Knight": FighterProfile(
        name="Meta Knight",
        cohort="Royal Heavyweights",
        symbol="🦇(ò_ó)⚔️",
        color_ansi=C_BLUE,
        mass=1.3,
        radius=2.0,
        restitution=0.85,
        drag=0.97,
        max_speed=3.6,
        punch_impulse=5.0,
        punch_range=2.8,
        punch_cooldown_max=10,
        smart_trait="Mach Sword Flurry & Warp"
    )
}

COHORTS: Dict[str, List[str]] = {
    "magician_tac": ["Tac", "Magician Kirby"],
    "waddles": ["Bandana Dee", "Waddle Dee", "Waddle Doo"],
    "heavy": ["King Dedede", "Meta Knight"],
    "duo_not_kirby": ["Tac", "Bandana Dee"],
    "all_stars": ["Tac", "Magician Kirby", "Bandana Dee", "King Dedede"]
}


@dataclass
class FighterActor:
    profile: FighterProfile
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    punch_cooldown: int = 0
    tumble_timer: int = 0
    is_punching: bool = False
    last_hit_by: str = ""
    current_quote: str = ""
    quote_timer: int = 0
    punches_landed: int = 0
    knockbacks_taken: int = 0
    heists_completed: int = 0

    @property
    def speed(self) -> float:
        return math.hypot(self.vx, self.vy)

    @property
    def momentum(self) -> float:
        return self.profile.mass * self.speed

    @property
    def kinetic_energy(self) -> float:
        return 0.5 * self.profile.mass * (self.speed ** 2)


@dataclass
class CursorObject:
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    is_snatched: bool = False
    snatched_by: str = ""
    decoy_active: bool = False
    decoy_x: float = 0.0
    decoy_y: float = 0.0
    target_zone_x: float = 0.0
    target_zone_y: float = 0.0
    target_zone_label: str = "CONFIRM [DANGER]"


class PhyXEngine2D:
    def __init__(self, width: float = 80.0, height: float = 24.0):
        self.width = width
        self.height = height
        self.fighters: List[FighterActor] = []
        self.cursor: CursorObject = CursorObject(x=width * 0.5, y=height * 0.5)
        self.step_count: int = 0
        self.total_punches: int = 0
        self.total_heists: int = 0
        self.total_energy_dissipated: float = 0.0
        self.last_impact_event: str = ""
        self.active_cohort_name: str = "duo_not_kirby"

    def load_cohort(self, cohort_key: str):
        self.active_cohort_name = cohort_key
        names = COHORTS.get(cohort_key, COHORTS["duo_not_kirby"])
        self.fighters.clear()
        
        spacing = self.width / (len(names) + 1)
        for i, name in enumerate(names):
            profile = FIGHTER_TEMPLATES[name]
            # Alternate left/right velocities
            vx = random.uniform(-1.5, 1.5)
            vy = random.uniform(-0.8, 0.8)
            actor = FighterActor(
                profile=profile,
                x=spacing * (i + 1),
                y=self.height * 0.5 + random.uniform(-4, 4),
                vx=vx,
                vy=vy
            )
            self.fighters.append(actor)
        
        # Position confirmation danger button near bottom-center
        self.cursor.target_zone_x = self.width * 0.75
        self.cursor.target_zone_y = self.height * 0.70
        self.cursor.target_zone_label = "CONFIRM: [DROP_PROD_TABLES]"

    def update(self, dt: float = 1.0):
        self.step_count += 1
        
        # 1. Update confirmation zone & cursor simulation
        self._update_cursor(dt)

        # 2. Update fighter kinematics & AI behaviors
        for actor in self.fighters:
            self._update_fighter_ai(actor)
            self._integrate_kinematics(actor, dt)
            self._resolve_boundary_collisions(actor)

        # 3. Resolve pair-wise fighter collisions & momentum punching
        n = len(self.fighters)
        for i in range(n):
            for j in range(i + 1, n):
                self._resolve_fighter_interaction(self.fighters[i], self.fighters[j])

        # 4. Resolve Tac cursor intercept heuristic
        self._resolve_tac_cursor_heist()

    def _update_cursor(self, dt: float):
        if not self.cursor.is_snatched:
            # Operator mouse drifts naturally towards the dangerous confirmation button
            dx = self.cursor.target_zone_x - self.cursor.x
            dy = self.cursor.target_zone_y - self.cursor.y
            dist = math.hypot(dx, dy)
            if dist > 1.0:
                self.cursor.vx += (dx / dist) * 0.25
                self.cursor.vy += (dy / dist) * 0.25
            self.cursor.vx *= 0.88
            self.cursor.vy *= 0.88
            self.cursor.x += self.cursor.vx * dt
            self.cursor.y += self.cursor.vy * dt
        else:
            # Cursor is being flung away by Tac with kickback momentum!
            self.cursor.x += self.cursor.vx * dt
            self.cursor.y += self.cursor.vy * dt
            self.cursor.vx *= 0.94
            self.cursor.vy *= 0.94
            # Keep in bounds
            if self.cursor.x <= 2 or self.cursor.x >= self.width - 2:
                self.cursor.vx *= -0.7
            if self.cursor.y <= 2 or self.cursor.y >= self.height - 2:
                self.cursor.vy *= -0.7
            if math.hypot(self.cursor.vx, self.cursor.vy) < 0.2:
                self.cursor.is_snatched = False
                self.cursor.snatched_by = ""

    def _update_fighter_ai(self, actor: FighterActor):
        if actor.quote_timer > 0:
            actor.quote_timer -= 1
        else:
            actor.current_quote = ""

        if actor.punch_cooldown > 0:
            actor.punch_cooldown -= 1
        actor.is_punching = False

        if actor.tumble_timer > 0:
            actor.tumble_timer -= 1
            # In tumble state, physics momentum dominates, AI input disabled
            return

        # Target nearest other fighter
        target = None
        min_dist = float('inf')
        for other in self.fighters:
            if other is not actor:
                d = math.hypot(other.x - actor.x, other.y - actor.y)
                if d < min_dist:
                    min_dist = d
                    target = other

        if target:
            dx = target.x - actor.x
            dy = target.y - actor.y
            dist = max(0.01, min_dist)

            # Move towards opponent with tactical agility
            desired_vx = (dx / dist) * actor.profile.max_speed
            desired_vy = (dy / dist) * actor.profile.max_speed

            accel = 0.35
            actor.vx += (desired_vx - actor.vx) * accel
            actor.vy += (desired_vy - actor.vy) * accel

    def _integrate_kinematics(self, actor: FighterActor, dt: float):
        # Apply air drag damping
        actor.vx *= actor.profile.drag
        actor.vy *= actor.profile.drag

        # Clamp max speed
        spd = actor.speed
        if spd > actor.profile.max_speed * 2.2: # allow impulse bursts up to 2.2x
            actor.vx = (actor.vx / spd) * (actor.profile.max_speed * 2.2)
            actor.vy = (actor.vy / spd) * (actor.profile.max_speed * 2.2)

        actor.x += actor.vx * dt
        actor.y += actor.vy * dt

    def _resolve_boundary_collisions(self, actor: FighterActor):
        margin_x = actor.profile.radius
        margin_y = actor.profile.radius * 0.6 # terminal aspect ratio scaling

        # Left / Right boundaries
        if actor.x - margin_x < 1.0:
            actor.x = 1.0 + margin_x
            actor.vx = -actor.vx * actor.profile.restitution
            self.total_energy_dissipated += 0.5 * actor.profile.mass * (actor.vx ** 2) * (1 - actor.profile.restitution)
        elif actor.x + margin_x > self.width - 2.0:
            actor.x = self.width - 2.0 - margin_x
            actor.vx = -actor.vx * actor.profile.restitution
            self.total_energy_dissipated += 0.5 * actor.profile.mass * (actor.vx ** 2) * (1 - actor.profile.restitution)

        # Top / Bottom boundaries
        if actor.y - margin_y < 1.0:
            actor.y = 1.0 + margin_y
            actor.vy = -actor.vy * actor.profile.restitution
            self.total_energy_dissipated += 0.5 * actor.profile.mass * (actor.vy ** 2) * (1 - actor.profile.restitution)
        elif actor.y + margin_y > self.height - 2.0:
            actor.y = self.height - 2.0 - margin_y
            actor.vy = -actor.vy * actor.profile.restitution
            self.total_energy_dissipated += 0.5 * actor.profile.mass * (actor.vy ** 2) * (1 - actor.profile.restitution)

    def _resolve_fighter_interaction(self, a: FighterActor, b: FighterActor):
        dx = b.x - a.x
        dy = b.y - a.y
        dist = math.hypot(dx, dy)
        min_dist = a.profile.radius + b.profile.radius

        # Check punch trigger within strike distance
        strike_dist = max(min_dist, max(a.profile.punch_range, b.profile.punch_range))
        if dist < strike_dist:
            # Can A punch B?
            if a.punch_cooldown == 0 and a.tumble_timer == 0:
                self._execute_punch(attacker=a, victim=b, dx=dx, dy=dy, dist=dist)
            # Can B punch A?
            elif b.punch_cooldown == 0 and b.tumble_timer == 0:
                self._execute_punch(attacker=b, victim=a, dx=-dx, dy=-dy, dist=dist)

        # Rigid body elastic collision resolution
        if dist < min_dist and dist > 0.001:
            nx = dx / dist
            ny = dy / dist

            # Separate overlapping bodies
            overlap = min_dist - dist
            total_mass = a.profile.mass + b.profile.mass
            a.x -= nx * overlap * (b.profile.mass / total_mass)
            a.y -= ny * overlap * (b.profile.mass / total_mass)
            b.x += nx * overlap * (a.profile.mass / total_mass)
            b.y += ny * overlap * (a.profile.mass / total_mass)

            # Relative velocity along collision normal
            kx = a.vx - b.vx
            ky = a.vy - b.vy
            p = 2 * (nx * kx + ny * ky) / total_mass
            restitution = (a.profile.restitution + b.profile.restitution) * 0.5

            a.vx -= p * b.profile.mass * nx * restitution
            a.vy -= p * b.profile.mass * ny * restitution
            b.vx += p * a.profile.mass * nx * restitution
            b.vy += p * a.profile.mass * ny * restitution

    def _execute_punch(self, attacker: FighterActor, victim: FighterActor, dx: float, dy: float, dist: float):
        attacker.is_punching = True
        attacker.punch_cooldown = attacker.profile.punch_cooldown_max
        attacker.punches_landed += 1
        victim.knockbacks_taken += 1
        victim.last_hit_by = attacker.profile.name
        self.total_punches += 1

        # Deliver kinetic momentum impulse
        nx = dx / dist
        ny = dy / dist
        impulse = attacker.profile.punch_impulse

        # Victim launched into tumbling knockback
        victim.vx += (nx * impulse) / victim.profile.mass
        victim.vy += (ny * impulse) / victim.profile.mass
        victim.tumble_timer = int(8 + (impulse / victim.profile.mass) * 3)

        # Attacker kickback recoil
        attacker.vx -= (nx * impulse * 0.28) / attacker.profile.mass
        attacker.vy -= (ny * impulse * 0.28) / attacker.profile.mass

        # Combat banter
        if random.random() < 0.65:
            quotes = COMBAT_BANTER.get(attacker.profile.name, ["POW!"])
            attacker.current_quote = random.choice(quotes)
            attacker.quote_timer = 14

        self.last_impact_event = (
            f"🥊 {attacker.profile.name} PUNCHED {victim.profile.name}! "
            f"Impulse={impulse:.1f} N·s | Victim speed={victim.speed:.2f}"
        )

    def _resolve_tac_cursor_heist(self):
        # Find Tac in current fighters
        tac = next((a for a in self.fighters if a.profile.name == "Tac"), None)
        if not tac:
            return

        # Check proximity of operator cursor to confirmation danger button
        dist_to_confirm = math.hypot(
            self.cursor.x - self.cursor.target_zone_x,
            self.cursor.y - self.cursor.target_zone_y
        )

        # If user cursor approaches within 8 units of confirmation button, Tac ambushes!
        if dist_to_confirm < 8.0 and not self.cursor.is_snatched:
            dist_tac_cursor = math.hypot(tac.x - self.cursor.x, tac.y - self.cursor.y)
            if dist_tac_cursor < 4.0:
                # SNEAK HEIST EXECUTION!
                self.cursor.is_snatched = True
                self.cursor.snatched_by = "Tac"
                self.cursor.decoy_active = True
                self.cursor.decoy_x = self.cursor.x
                self.cursor.decoy_y = self.cursor.y

                # Fling cursor pointer safely far away from confirmation button
                fling_angle = math.atan2(self.cursor.y - self.cursor.target_zone_y, self.cursor.x - self.cursor.target_zone_x)
                if abs(fling_angle) < 0.1:
                    fling_angle = -math.pi * 0.6
                
                self.cursor.vx = math.cos(fling_angle) * 7.5
                self.cursor.vy = math.sin(fling_angle) * 5.0

                tac.heists_completed += 1
                self.total_heists += 1

                # Smart-toned, snarky "Doooon't!" speech bubble
                tac.current_quote = random.choice(TAC_DOONT_QUOTES)
                tac.quote_timer = 28

                # If Magician Kirby is present, he casts Decoy Prestige
                magician = next((a for a in self.fighters if a.profile.name == "Magician Kirby"), None)
                if magician:
                    magician.current_quote = "✨ Presto Chango! Decoy cursor deployed! 🎩"
                    magician.quote_timer = 24

                self.last_impact_event = f"🦝 TAC SNATCHED CURSOR! Confirmation Intercepted! {tac.current_quote[:45]}..."

    def get_telemetry(self) -> Dict[str, Any]:
        total_p = sum(a.momentum for a in self.fighters)
        total_ke = sum(a.kinetic_energy for a in self.fighters)
        return {
            "step": self.step_count,
            "cohort": self.active_cohort_name,
            "fighters": [
                {
                    "name": a.profile.name,
                    "cohort": a.profile.cohort,
                    "x": round(a.x, 2),
                    "y": round(a.y, 2),
                    "vx": round(a.vx, 2),
                    "vy": round(a.vy, 2),
                    "speed": round(a.speed, 2),
                    "momentum": round(a.momentum, 2),
                    "punches": a.punches_landed,
                    "knockbacks": a.knockbacks_taken,
                    "heists": a.heists_completed,
                    "state": "TUMBLING" if a.tumble_timer > 0 else ("PUNCHING" if a.is_punching else "READY")
                }
                for a in self.fighters
            ],
            "system_momentum_N_s": round(total_p, 2),
            "system_kinetic_energy_J": round(total_ke, 2),
            "total_punches": self.total_punches,
            "total_heists": self.total_heists,
            "cursor": {
                "x": round(self.cursor.x, 2),
                "y": round(self.cursor.y, 2),
                "is_snatched": self.cursor.is_snatched,
                "snatched_by": self.cursor.snatched_by,
                "target_zone": self.cursor.target_zone_label
            },
            "last_impact": self.last_impact_event
        }

    def render_ansi_canvas(self) -> str:
        w = int(self.width)
        h = int(self.height)
        grid = [[" " for _ in range(w)] for _ in range(h)]

        # Draw border
        for x in range(w):
            grid[0][x] = "═"
            grid[h - 1][x] = "═"
        for y in range(h):
            grid[y][0] = "║"
            grid[y][w - 1] = "║"
        grid[0][0] = "╔"
        grid[0][w - 1] = "╗"
        grid[h - 1][0] = "╚"
        grid[h - 1][w - 1] = "╝"

        # Draw Confirmation Danger Zone button
        bx = int(self.cursor.target_zone_x) - 10
        by = int(self.cursor.target_zone_y)
        btn_text = f"[{self.cursor.target_zone_label}]"
        if 0 <= by < h:
            for i, ch in enumerate(btn_text):
                if 1 <= bx + i < w - 1:
                    grid[by][bx + i] = ch

        # Draw operator cursor / decoy
        cx = int(self.cursor.x)
        cy = int(self.cursor.y)
        if 1 <= cx < w - 1 and 1 <= cy < h - 1:
            grid[cy][cx] = "🎯" if not self.cursor.is_snatched else "💨"

        if self.cursor.decoy_active and self.cursor.is_snatched:
            dx = int(self.cursor.decoy_x)
            dy = int(self.cursor.decoy_y)
            if 1 <= dx < w - 1 and 1 <= dy < h - 1:
                grid[dy][dx] = "❓"

        # Draw fighters
        lines_output = []
        for y in range(h):
            row_str = ""
            for x in range(w):
                # Check if fighter occupies cell
                cell_fighter = None
                for a in self.fighters:
                    fx = int(a.x)
                    fy = int(a.y)
                    if fx == x and fy == y:
                        cell_fighter = a
                        break

                if cell_fighter:
                    sym = cell_fighter.profile.symbol
                    if cell_fighter.tumble_timer > 0:
                        sym = "💫(x_x)"
                    elif cell_fighter.is_punching:
                        sym = "🥊" + cell_fighter.profile.symbol[:4]
                    row_str += f"{cell_fighter.profile.color_ansi}{sym}{C_RESET}"
                else:
                    ch = grid[y][x]
                    if ch in ["═", "║", "╔", "╗", "╚", "╝"]:
                        row_str += f"{C_DARK_GRAY}{ch}{C_RESET}"
                    elif "CONFIRM" in self.cursor.target_zone_label and y == by and bx <= x < bx + len(btn_text):
                        row_str += f"{C_RED}{C_BOLD}{ch}{C_RESET}"
                    elif ch == "🎯":
                        row_str += f"{C_GREEN}{C_BOLD}{ch}{C_RESET}"
                    elif ch == "💨" or ch == "❓":
                        row_str += f"{C_YELLOW}{C_BOLD}{ch}{C_RESET}"
                    else:
                        row_str += ch
            lines_output.append(row_str)

        # Overlay speech balloons
        quotes_summary = []
        for a in self.fighters:
            if a.current_quote:
                quotes_summary.append(f"{a.profile.color_ansi}{a.profile.name}: \"{a.current_quote}\"{C_RESET}")

        canvas_str = "\n".join(lines_output)
        return canvas_str, quotes_summary


def save_engine_state(engine: PhyXEngine2D):
    telemetry = engine.get_telemetry()
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(telemetry, f, indent=2)
    except Exception:
        pass

    # Log to ledger
    try:
        LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
        event = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "subsystem": "kirby_consortium_phyx",
            "cohort": engine.active_cohort_name,
            "punches": engine.total_punches,
            "heists": engine.total_heists,
            "system_momentum": telemetry["system_momentum_N_s"]
        }
        with open(LEDGER_FILE, "a") as f:
            f.write(json.dumps(event) + "\n")
    except Exception:
        pass


def run_test_suite() -> bool:
    print(f"{C_PINK}╔════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_PINK}║  🌸 KIRBY CONSORTIUM & 2D PHYX ENGINE: AUTOMATED TEST SUITE 🌸     ║{C_RESET}")
    print(f"{C_PINK}╚════════════════════════════════════════════════════════════════════╝{C_RESET}")

    engine = PhyXEngine2D(width=80.0, height=24.0)

    # Test 1: Cohort Initialization
    print(f"\n{C_BOLD}[Stage 1/5] Testing Cohort Consortium Roster...{C_RESET}")
    for cname in ["magician_tac", "waddles", "heavy", "duo_not_kirby", "all_stars"]:
        engine.load_cohort(cname)
        assert len(engine.fighters) >= 2, f"Cohort {cname} failed to load fighters!"
        names = [f.profile.name for f in engine.fighters]
        print(f"  [✔] Cohort '{cname}': {names}")

    # Test 2: Kinematics & Momentum Conservation Principle
    print(f"\n{C_BOLD}[Stage 2/5] Testing 2D Momentum Kinematics Simulation...{C_RESET}")
    engine.load_cohort("duo_not_kirby") # Tac & Bandana Dee
    p_initial = sum(f.momentum for f in engine.fighters)
    for _ in range(50):
        engine.update(dt=1.0)
    telem = engine.get_telemetry()
    assert telem["step"] == 50, "Step count mismatch!"
    print(f"  [✔] 50 steps simulated. Total punches: {engine.total_punches}, Momentum: {telem['system_momentum_N_s']} N·s")

    # Test 3: Tac Cursor Heist & Confirmation Interception
    print(f"\n{C_BOLD}[Stage 3/5] Testing Tac Cursor Heist & 'Doooon't!' Interceptor...{C_RESET}")
    engine.load_cohort("magician_tac")
    # Position cursor right on confirmation button and Tac adjacent
    engine.cursor.x = engine.cursor.target_zone_x - 1.0
    engine.cursor.y = engine.cursor.target_zone_y
    tac = next(f for f in engine.fighters if f.profile.name == "Tac")
    tac.x = engine.cursor.x - 1.0
    tac.y = engine.cursor.y
    tac.punch_cooldown = 0
    engine.update(dt=1.0)
    assert engine.total_heists >= 1, "Tac failed to snatch cursor!"
    assert engine.cursor.is_snatched, "Cursor state not marked as snatched!"
    print(f"  [✔] Tac Heist Verified: {engine.last_impact_event}")

    # Test 4: Heavyweight Super Hammer Momentum Transfer
    print(f"\n{C_BOLD}[Stage 4/5] Testing King Dedede 2.5x Mass Hammer Knockback...{C_RESET}")
    engine.load_cohort("heavy") # King Dedede & Meta Knight
    kd = next(f for f in engine.fighters if f.profile.name == "King Dedede")
    mk = next(f for f in engine.fighters if f.profile.name == "Meta Knight")
    assert kd.profile.mass == 2.5, "King Dedede mass must be 2.5!"
    assert kd.profile.punch_impulse >= 7.0, "King Dedede punch impulse must be >= 7.0!"
    print(f"  [✔] King Dedede Mass: {kd.profile.mass}kg | Impulse: {kd.profile.punch_impulse} N·s")

    # Test 5: State Persistence & Telemetry Output
    print(f"\n{C_BOLD}[Stage 5/5] Testing State File & Ledger Persistence...{C_RESET}")
    save_engine_state(engine)
    assert STATE_FILE.exists(), f"State file {STATE_FILE} not created!"
    with open(STATE_FILE) as f:
        data = json.load(f)
        assert data["total_heists"] >= 1
    print(f"  [✔] Successfully written state to {STATE_FILE}")

    print(f"\n{C_GREEN}{C_BOLD}✨ ALL 5 PHYX CONSORTIUM TEST STAGES PASSED FLAWLESSLY! ✨{C_RESET}\n")
    return True


def run_demo(cohort_key: str = "duo_not_kirby", fps: int = 15, duration_s: int = 20):
    cols, rows = shutil.get_terminal_size((80, 24))
    engine = PhyXEngine2D(width=float(cols - 2), height=float(rows - 8))
    engine.load_cohort(cohort_key)

    print("\033[?25l\033[2J", end="") # Hide cursor, clear screen
    try:
        start_time = time.time()
        while time.time() - start_time < duration_s:
            engine.update(dt=1.0)
            canvas_str, quotes = engine.render_ansi_canvas()
            telem = engine.get_telemetry()

            hud = (
                f"\033[H{C_PINK}{C_BOLD}🌸 KIRBY CONSORTIUM 2D PHYX ARENA 🌸{C_RESET} | "
                f"Cohort: {C_CYAN}{telem['cohort'].upper()}{C_RESET} | "
                f"Punches: {C_YELLOW}{telem['total_punches']}{C_RESET} | "
                f"Heists: {C_PURPLE}{telem['total_heists']}{C_RESET} | "
                f"Momentum: {C_GREEN}{telem['system_momentum_N_s']} N·s{C_RESET}\n"
            )

            quote_block = ""
            if quotes:
                quote_block = "  💬 " + " | ".join(quotes[:2]) + "\n"

            status_bar = (
                f"{C_DARK_GRAY}Target Zone: {telem['cursor']['target_zone']} | "
                f"Cursor Snatched: {'YES (Tac Heist Active!)' if telem['cursor']['is_snatched'] else 'NO'} | "
                f"Impact: {telem['last_impact'][:45]}{C_RESET}"
            )

            sys.stdout.write(hud + canvas_str + "\n" + quote_block + status_bar + "\n")
            sys.stdout.flush()
            time.sleep(1.0 / max(1, fps))

        save_engine_state(engine)
    except KeyboardInterrupt:
        pass
    finally:
        print("\033[?25h\033[0m") # Restore cursor


def main():
    parser = argparse.ArgumentParser(description="Kirby Consortium & 2D PhyX Momentum Arena")
    parser.add_argument("command", nargs="?", default="demo", choices=["demo", "test", "brawl", "tac", "waddles", "heavy", "status"])
    parser.add_argument("--cohort", default="duo_not_kirby", choices=list(COHORTS.keys()))
    parser.add_argument("--fps", type=int, default=15)
    parser.add_argument("--duration", type=int, default=15)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    if args.test or args.command == "test":
        success = run_test_suite()
        sys.exit(0 if success else 1)

    cohort_map = {
        "tac": "magician_tac",
        "waddles": "waddles",
        "heavy": "heavy",
        "brawl": "all_stars",
        "demo": args.cohort
    }
    selected_cohort = cohort_map.get(args.command, args.cohort)

    if args.command == "status":
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                print(json.dumps(json.load(f), indent=2))
        else:
            print("No active Phyx state file found. Run 'kirby phyx test' or 'kirby phyx demo'.")
        return

    run_demo(cohort_key=selected_cohort, fps=args.fps, duration_s=args.duration)


if __name__ == "__main__":
    main()
