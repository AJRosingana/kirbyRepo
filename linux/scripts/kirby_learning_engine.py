#!/usr/bin/env python3
"""
🌸 KIRBY AUTOPOIETIC LEARNING & EVENT RESPONSE ENGINE 🌸
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_learning_engine.py
Unified CLI: kirby learn | kirby cards | kirby event | kirby synthesize

Features:
1. Dynamic Action Card Learning & Ability Synthesis (Inhale & Fusion Matrix)
2. Reactive Event Response Engine (System Telemetry, User Gestures, Mesh Ingress)
3. Multi-Tier Mastery & XP Progression (Lv 1 -> Lv 5, Multipliers, Cooldowns)
4. Persistent Evolutionary Ledger in ledger/kirby_learning_ledger.jsonl
5. Real-Time Synchronization with kirby_action_cards.json & kirby_motion_deck.json
6. ANSI Illustrated ASCII Card Visualizer & Foley Acoustics Integration
================================================================================
"""

import os
import sys
import time
import json
import random
import argparse
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Any

# ANSI Palette
C_PINK = "\033[38;5;205m"
C_CYAN = "\033[38;5;81m"
C_YELLOW = "\033[38;5;220m"
C_GREEN = "\033[38;5;120m"
C_PURPLE = "\033[38;5;141m"
C_ORANGE = "\033[38;5;208m"
C_RED = "\033[38;5;196m"
C_WHITE = "\033[38;5;255m"
C_DIM = "\033[2m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"

BASE_DIR = Path("/mnt/shared/AntiGravity_Shared")
CARDS_FILE = BASE_DIR / "kirby_action_cards.json"
MOTION_DECK_FILE = BASE_DIR / "kirby_motion_deck.json"
LEDGER_DIR = BASE_DIR / "ledger"
LEDGER_FILE = LEDGER_DIR / "kirby_learning_ledger.jsonl"

# Audio FX Integration
HAS_AUDIO = False
try:
    sys.path.insert(0, str(BASE_DIR))
    from agy_fx_engine import play_sound_preset
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False


def ensure_paths():
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    if not CARDS_FILE.exists():
        sys.stderr.write(f"Warning: {CARDS_FILE} not found!\n")


def load_cards_registry() -> Dict[str, Any]:
    ensure_paths()
    if CARDS_FILE.exists():
        try:
            with open(CARDS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            sys.stderr.write(f"Error loading {CARDS_FILE}: {e}\n")
    return {"deckName": "Kirby Unified Action Cards", "version": "3.0.0", "cards": [], "eventResponseMatrix": {}}


def save_cards_registry(registry: Dict[str, Any]):
    registry["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    registry["totalCards"] = len(registry.get("cards", []))
    with open(CARDS_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)


def record_learning_ledger(entry: Dict[str, Any]):
    ensure_paths()
    entry["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(LEDGER_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def render_ascii_card(card: Dict[str, Any], banner_title: str = "🌸 ACTION CARD DRAWN 🌸") -> str:
    card_id = card.get("id", "UNKNOWN")
    name = card.get("name", "Unnamed Card")
    icon = card.get("icon", "⭐")
    ap = card.get("costAP", 1)
    cooldown = card.get("cooldown", 1.0)
    category = card.get("abilityCategory", "GENERAL")
    desc = card.get("description", "No description.")
    speech = card.get("speech", "Poyo! ✨")
    level = card.get("masteryLevel", 1)
    color = card.get("auraColor", "#ff79c6")
    triggers = ", ".join(card.get("eventTriggers", [])[:2])

    stars = "★" * level + "☆" * (5 - level)

    lines = [
        f"{C_BOLD}{C_PINK}╔════════════════════════════════════════════════════════════════╗{C_RESET}",
        f"{C_BOLD}{C_PINK}║ {C_YELLOW}{banner_title.center(62)}{C_PINK} ║{C_RESET}",
        f"{C_BOLD}{C_PINK}╠════════════════════════════════════════════════════════════════╣{C_RESET}",
        f"{C_BOLD}{C_PINK}║ {C_WHITE}{icon} {C_BOLD}{name:<32}{C_YELLOW}Cost: {ap} AP  {C_CYAN}CD: {cooldown}s{C_PINK} ║{C_RESET}",
        f"{C_BOLD}{C_PINK}║ {C_PURPLE}Category: {category:<20}{C_GREEN}Mastery: {stars} (Lv.{level}){C_PINK} ║{C_RESET}",
        f"{C_BOLD}{C_PINK}╟────────────────────────────────────────────────────────────────╢{C_RESET}",
    ]

    # Description wrapping
    words = desc.split()
    cur_line = ""
    for w in words:
        if len(cur_line) + len(w) + 1 <= 60:
            cur_line += (" " if cur_line else "") + w
        else:
            lines.append(f"{C_BOLD}{C_PINK}║ {C_WHITE}{cur_line:<62}{C_PINK} ║{C_RESET}")
            cur_line = w
    if cur_line:
        lines.append(f"{C_BOLD}{C_PINK}║ {C_WHITE}{cur_line:<62}{C_PINK} ║{C_RESET}")

    lines.append(f"{C_BOLD}{C_PINK}╟────────────────────────────────────────────────────────────────╢{C_RESET}")
    lines.append(f"{C_BOLD}{C_PINK}║ {C_CYAN}Overhead Speech: {C_WHITE}\"{speech}\"{C_PINK:<12} ║{C_RESET}")
    if triggers:
        lines.append(f"{C_BOLD}{C_PINK}║ {C_YELLOW}Triggers: {triggers:<52}{C_PINK} ║{C_RESET}")
    lines.append(f"{C_BOLD}{C_PINK}╚════════════════════════════════════════════════════════════════╝{C_RESET}")

    return "\n".join(lines)


class KirbyLearningEngine:
    def __init__(self):
        self.registry = load_cards_registry()

    def list_cards(self) -> List[Dict[str, Any]]:
        return self.registry.get("cards", [])

    def get_card(self, card_id: str) -> Optional[Dict[str, Any]]:
        for c in self.registry.get("cards", []):
            if c.get("id") == card_id or c.get("name", "").lower() == card_id.lower():
                return c
        return None

    def draw_card(self) -> Dict[str, Any]:
        cards = self.list_cards()
        if not cards:
            raise ValueError("Action Deck is empty!")
        weights = [c.get("baseProbability", 0.05) for c in cards]
        total_w = sum(weights)
        if total_w > 0:
            norm_weights = [w / total_w for w in weights]
            selected = random.choices(cards, weights=norm_weights, k=1)[0]
        else:
            selected = random.choice(cards)

        # Increment times triggered
        selected["timesTriggered"] = selected.get("timesTriggered", 0) + 1
        save_cards_registry(self.registry)
        return selected

    def execute_card(self, card_id: str) -> Dict[str, Any]:
        card = self.get_card(card_id)
        if not card:
            raise ValueError(f"Action card '{card_id}' not found in registry!")

        card["timesTriggered"] = card.get("timesTriggered", 0) + 1
        xp_gain = 25 * card.get("masteryLevel", 1)
        stats = self.registry.get("learningStats", {})
        stats["totalXp"] = stats.get("totalXp", 0) + xp_gain

        # Check for level up
        if card["timesTriggered"] % 15 == 0 and card.get("masteryLevel", 1) < 5:
            card["masteryLevel"] = card.get("masteryLevel", 1) + 1
            card["cooldown"] = max(0.5, round(card.get("cooldown", 1.5) * 0.85, 2))
            level_up = True
        else:
            level_up = False

        save_cards_registry(self.registry)

        # Audio playback if present
        sound = card.get("soundFx", "poyo")
        if HAS_AUDIO:
            try:
                play_sound_preset(sound)
            except Exception:
                pass

        # Record in ledger
        record_learning_ledger({
            "action": "EXECUTE_CARD",
            "cardId": card["id"],
            "name": card["name"],
            "xpGained": xp_gain,
            "levelUp": level_up,
            "masteryLevel": card.get("masteryLevel", 1),
            "timesTriggered": card["timesTriggered"]
        })

        return {
            "card": card,
            "xpGain": xp_gain,
            "levelUp": level_up,
            "speech": card.get("speech", "Poyo! ✨"),
            "haptic": card.get("hapticProfile", "detentTick"),
            "sound": sound
        }

    def dispatch_event(self, event_name: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        matrix = self.registry.get("eventResponseMatrix", {})
        event_name = event_name.upper()
        if not event_name.startswith("EVENT_"):
            event_name = "EVENT_" + event_name

        response_rule = matrix.get(event_name)
        if not response_rule:
            # Fallback search through eventTriggers in cards
            matching_cards = [
                c for c in self.list_cards()
                if event_name in c.get("eventTriggers", [])
            ]
            if matching_cards:
                selected_card = random.choice(matching_cards)
                response_rule = {
                    "primaryCard": selected_card["id"],
                    "speech": selected_card.get("speech", "Poyo! Responding to event!"),
                    "haptic": selected_card.get("hapticProfile", "detentTick"),
                    "sound": selected_card.get("soundFx", "poyo")
                }
            else:
                # Default generic fallback
                response_rule = {
                    "primaryCard": "card_warp",
                    "speech": f"Poyo! Observed {event_name}! Adapting flight pattern!",
                    "haptic": "detentTick",
                    "sound": "fanfare"
                }

        primary_id = response_rule.get("primaryCard", "card_warp")
        card = self.get_card(primary_id) or self.list_cards()[0]

        execution = self.execute_card(card["id"])

        record_learning_ledger({
            "action": "EVENT_RESPONSE_DISPATCHED",
            "event": event_name,
            "cardId": card["id"],
            "speech": response_rule.get("speech"),
            "payload": payload or {}
        })

        return {
            "event": event_name,
            "card": card,
            "rule": response_rule,
            "execution": execution,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    def synthesize_abilities(self, card_id_a: str, card_id_b: str) -> Dict[str, Any]:
        card_a = self.get_card(card_id_a)
        card_b = self.get_card(card_id_b)
        if not card_a or not card_b:
            raise ValueError(f"Both cards must exist to synthesize! (Found: {card_id_a}={bool(card_a)}, {card_id_b}={bool(card_b)})")

        if card_a["id"] == card_b["id"]:
            raise ValueError("Cannot synthesize a card with itself! Choose two distinct abilities.")

        cat_a = card_a.get("abilityCategory", "ABILITY_A")
        cat_b = card_b.get("abilityCategory", "ABILITY_B")

        # Deterministic hybrid ID
        sorted_ids = sorted([card_a['id'].replace('card_', ''), card_b['id'].replace('card_', '')])
        hybrid_id = f"card_hybrid_{sorted_ids[0]}_{sorted_ids[1]}"

        # Check if already exists
        existing = self.get_card(hybrid_id)
        if existing:
            return {"status": "ALREADY_SYNTHESIZED", "card": existing}

        name_combo = f"{card_a['name'].split()[0]} {card_b['name'].split()[-1]} Fusion"
        icon_combo = f"{card_a.get('icon', '⭐')}{card_b.get('icon', '✨')}"
        cost_ap = max(1, min(4, (card_a.get("costAP", 1) + card_b.get("costAP", 1)) // 2 + 1))
        cooldown = round((card_a.get("cooldown", 1.5) + card_b.get("cooldown", 1.5)) / 2.0, 1)

        combined_triggers = list(set(card_a.get("eventTriggers", []) + card_b.get("eventTriggers", [])))

        speech = f"SUPER SYNTHESIS! {name_combo}! Sparking cosmic synergy! {icon_combo}"
        desc = f"[Learned Synthesis: {card_a['name']} + {card_b['name']}] Combines {cat_a} and {cat_b} for devastating multi-phase impact."

        hybrid_card = {
            "id": hybrid_id,
            "name": name_combo,
            "icon": icon_combo,
            "abilityCategory": "HYBRID_SYNTHESIS",
            "costAP": cost_ap,
            "cooldown": cooldown,
            "hotkey": "?",
            "description": desc,
            "speech": speech,
            "auraColor": card_a.get("auraColor", "#ec4899"),
            "hapticProfile": "seismicRumble",
            "soundFx": card_b.get("soundFx", "laser"),
            "speedX": (card_a.get("speedX", 5) + card_b.get("speedX", 5)) // 2,
            "speedY": (card_a.get("speedY", 0) + card_b.get("speedY", 0)) // 2,
            "durationTicks": max(card_a.get("durationTicks", 30), card_b.get("durationTicks", 30)),
            "baseProbability": 0.04,
            "eventTriggers": combined_triggers,
            "synergyRecipe": [card_a["id"], card_b["id"]],
            "masteryLevel": 1,
            "timesTriggered": 0
        }

        self.registry["cards"].append(hybrid_card)
        stats = self.registry.get("learningStats", {})
        stats["synthesizedCardsCount"] = stats.get("synthesizedCardsCount", 0) + 1
        stats["totalXp"] = stats.get("totalXp", 0) + 150
        save_cards_registry(self.registry)

        # Record in ledger
        record_learning_ledger({
            "action": "SYNTHESIS_DISCOVERY",
            "hybridId": hybrid_id,
            "name": name_combo,
            "ingredients": [card_a["id"], card_b["id"]],
            "xpGained": 150
        })

        return {"status": "NEWLY_SYNTHESIZED", "card": hybrid_card}

    def run_curiosity_learning_step(self) -> Dict[str, Any]:
        """Autonomous curiosity & reinforcement iteration."""
        # 1. Sample telemetry & environmental state
        now = time.time()
        load_avg = 0.5
        try:
            with open("/proc/loadavg") as f:
                load_avg = float(f.read().split()[0])
        except Exception:
            pass

        # 2. Pick learning archetype
        archetypes = ["SYNTHESIS", "REFINEMENT", "ADAPTATION", "TELEMETRY_MAPPING"]
        chosen_type = random.choice(archetypes)

        all_cards = self.list_cards()
        learned_item = {}

        if chosen_type == "SYNTHESIS" and len(all_cards) >= 2:
            a, b = random.sample(all_cards, 2)
            try:
                synth = self.synthesize_abilities(a["id"], b["id"])
                learned_item = {
                    "type": "SYNTHESIS",
                    "card": synth["card"],
                    "summary": f"Synthesized '{synth['card']['name']}' from {a['name']} + {b['name']}"
                }
            except Exception:
                chosen_type = "REFINEMENT"

        if chosen_type == "REFINEMENT":
            target_card = random.choice(all_cards)
            target_card["timesTriggered"] = target_card.get("timesTriggered", 0) + 3
            target_card["masteryLevel"] = min(5, target_card.get("masteryLevel", 1) + 1)
            target_card["cooldown"] = max(0.4, round(target_card.get("cooldown", 1.5) * 0.9, 2))
            save_cards_registry(self.registry)
            learned_item = {
                "type": "REFINEMENT",
                "card": target_card,
                "summary": f"Refined card '{target_card['name']}' to Mastery Lv.{target_card['masteryLevel']} (CD: {target_card['cooldown']}s)"
            }

        elif chosen_type == "ADAPTATION":
            # Formulate a new contextual event response card
            sample_concepts = [
                ("Chrono Starlight Dial", "⏳⭐", "TEMPORAL", "Accelerates asynchronous background job scheduling."),
                ("Prismatic Crystal Prism", "💎✨", "PRISMATIC", "Focuses ambient display photons into concentrated laser rays."),
                ("Quantum Foam Glider", "🌌🛸", "QUANTUM", "Phases through display boundaries and nullifies collision lag."),
                ("Nebula Cotton Cloud", "☁️🌸", "ATMOSPHERIC", "Deploys a bouncy fluffy cloud absorbing user drops.")
            ]
            cand = random.choice(sample_concepts)
            new_id = f"card_learned_{cand[0].lower().replace(' ', '_')}"
            if not self.get_card(new_id):
                new_card = {
                    "id": new_id,
                    "name": cand[0],
                    "icon": cand[1],
                    "abilityCategory": cand[2],
                    "costAP": 2,
                    "cooldown": 2.5,
                    "hotkey": "?",
                    "description": f"[Learned Discovery] {cand[3]}",
                    "speech": f"Poyo! Discovered {cand[0]}! {cand[1]}",
                    "auraColor": "#f472b6",
                    "hapticProfile": "starlightShimmer",
                    "soundFx": "fanfare",
                    "speedX": random.randint(2, 10),
                    "speedY": random.randint(-4, 4),
                    "durationTicks": 40,
                    "baseProbability": 0.05,
                    "eventTriggers": ["EVENT_TASK_COMPLETE", "EVENT_CHAOS_BURST"],
                    "synergyRecipe": None,
                    "masteryLevel": 1,
                    "timesTriggered": 1
                }
                self.registry["cards"].append(new_card)
                save_cards_registry(self.registry)
                learned_item = {
                    "type": "ADAPTATION",
                    "card": new_card,
                    "summary": f"Autopoietically invented brand-new Action Card '{new_card['name']}' ({new_card['icon']})"
                }
            else:
                learned_item = {
                    "type": "REINFORCED",
                    "card": self.get_card(new_id),
                    "summary": f"Reinforced existing invariant for '{cand[0]}'"
                }

        elif chosen_type == "TELEMETRY_MAPPING":
            # Map an unhandled event to an existing card
            sample_events = ["EVENT_CPU_SURGE", "EVENT_VIRTIOFS_BURST", "EVENT_WIFI_HANDOFF", "EVENT_GESTURE_TRIPLE_FLICK"]
            ev = random.choice(sample_events)
            card = random.choice(all_cards)
            if ev not in card.get("eventTriggers", []):
                card.setdefault("eventTriggers", []).append(ev)
                self.registry.setdefault("eventResponseMatrix", {})[ev] = {
                    "primaryCard": card["id"],
                    "speech": f"Poyo! Learned reactive response for {ev}! Deploying {card['name']}! {card.get('icon', '🌸')}",
                    "haptic": card.get("hapticProfile", "detentTick"),
                    "sound": card.get("soundFx", "poyo")
                }
                save_cards_registry(self.registry)
                learned_item = {
                    "type": "TELEMETRY_MAPPING",
                    "event": ev,
                    "card": card,
                    "summary": f"Learned dynamic event mapping: {ev} -> {card['name']}"
                }
            else:
                learned_item = {
                    "type": "MAPPING_VERIFIED",
                    "event": ev,
                    "card": card,
                    "summary": f"Verified event invariant {ev}"
                }

        # Gain global XP
        stats = self.registry.get("learningStats", {})
        stats["totalXp"] = stats.get("totalXp", 0) + 50
        save_cards_registry(self.registry)

        record_learning_ledger({
            "action": "CURIOSITY_LEARNING_STEP",
            "archetype": chosen_type,
            "details": learned_item.get("summary", ""),
            "loadAvg": load_avg
        })

        return learned_item


def main():
    parser = argparse.ArgumentParser(description="Kirby Autopoietic Learning & Action Deck Engine")
    subparsers = parser.add_subparsers(dest="subcommand", help="Command to execute")

    # list
    subparsers.add_parser("list", help="List all action cards in the active deck")

    # draw
    subparsers.add_parser("draw", help="Draw a random card and render ASCII frame")

    # play
    p_play = subparsers.add_parser("play", help="Execute an action card by ID or name")
    p_play.add_argument("card_id", help="Card ID or name to execute")

    # event
    p_event = subparsers.add_parser("event", help="Trigger an event and invoke Kirby's response")
    p_event.add_argument("event_name", help="Event name (e.g. THERMAL_SPIKE, VISITOR_ARRIVED)")

    # synthesize
    p_synth = subparsers.add_parser("synthesize", help="Fuse two abilities into a hybrid card")
    p_synth.add_argument("card_a", help="First ability card ID")
    p_synth.add_argument("card_b", help="Second ability card ID")

    # learn
    p_learn = subparsers.add_parser("learn", help="Run curiosity learning cycle")
    p_learn.add_argument("--count", "-n", type=int, default=1, help="Number of learning steps to execute")

    # ledger
    subparsers.add_parser("ledger", help="View recent entries in the evolutionary learning ledger")

    args = parser.parse_args()
    engine = KirbyLearningEngine()

    if args.subcommand == "list" or not args.subcommand:
        cards = engine.list_cards()
        stats = engine.registry.get("learningStats", {})
        print(f"\n{C_BOLD}{C_PINK}⭐ 🌸 KIRBY ACTION DECK & EVENT RESPONSE REGISTRY 🌸 ⭐{C_RESET}")
        print(f"{C_CYAN}Active Cards: {len(cards)} | Total XP: {stats.get('totalXp', 0)} | Mastery Level: {stats.get('masteryLevel', 1)}{C_RESET}\n")
        print(f"{'ID':<25} {'NAME':<28} {'ICON':<6} {'AP':<5} {'CD':<6} {'CATEGORY':<18} {'LVL'}")
        print(f"{'─'*25} {'─'*28} {'─'*6} {'─'*5} {'─'*6} {'─'*18} {'─'*5}")
        for c in cards:
            cid = c.get("id", "")
            name = c.get("name", "")
            icon = c.get("icon", "⭐")
            ap = str(c.get("costAP", 1))
            cd = f"{c.get('cooldown', 1.0)}s"
            cat = c.get("abilityCategory", "BASE")
            lvl = f"Lv.{c.get('masteryLevel', 1)}"
            print(f"{C_CYAN}{cid:<25}{C_WHITE}{name:<28}{icon:<6}{C_YELLOW}{ap:<5}{C_DIM}{cd:<6}{C_PURPLE}{cat:<18}{C_GREEN}{lvl}{C_RESET}")
        print()

    elif args.subcommand == "draw":
        drawn = engine.draw_card()
        print(render_ascii_card(drawn, "🌸 CARD DRAWN FROM ACTION DECK 🌸"))

    elif args.subcommand == "play":
        res = engine.execute_card(args.card_id)
        c = res["card"]
        print(render_ascii_card(c, f"⚔️ EXECUTING: {c['name'].upper()} ⚔️"))
        print(f"{C_GREEN}[✔] Action executed! Overhead Bubble: \"{res['speech']}\"{C_RESET}")
        print(f"    Haptic Profile: {C_YELLOW}{res['haptic']}{C_RESET} | Sound: {C_CYAN}{res['sound']}{C_RESET} | XP: +{res['xpGain']}")
        if res.get("levelUp"):
            print(f"    {C_BOLD}{C_YELLOW}🎉 LEVEL UP! Card reached Mastery Level {c.get('masteryLevel')}! Cooldown reduced to {c.get('cooldown')}s!{C_RESET}")

    elif args.subcommand == "event":
        res = engine.dispatch_event(args.event_name)
        c = res["card"]
        print(f"\n{C_BOLD}{C_YELLOW}⚡ INCOMING EVENT: {res['event']} ⚡{C_RESET}")
        print(render_ascii_card(c, f"🌸 REACTIVE RESPONSE: {c['name'].upper()} 🌸"))
        print(f"{C_GREEN}[✔] Reactive Response Triggered!{C_RESET}")
        print(f"    Dialogue: {C_WHITE}\"{res['rule'].get('speech')}\"{C_RESET}")
        print(f"    Haptic Feedback: {C_YELLOW}{res['rule'].get('haptic')}{C_RESET} | Sound: {C_CYAN}{res['rule'].get('sound')}{C_RESET}\n")

    elif args.subcommand == "synthesize":
        res = engine.synthesize_abilities(args.card_a, args.card_b)
        c = res["card"]
        status = res["status"]
        if status == "NEWLY_SYNTHESIZED":
            print(render_ascii_card(c, "✨ NEW HYBRID ACTION CARD SYNTHESIZED! ✨"))
            print(f"{C_BOLD}{C_GREEN}[✔] Success! Learned new fusion ability: {c['name']} ({c['icon']}){C_RESET}")
        else:
            print(render_ascii_card(c, "✨ EXISTING HYBRID CARD RETRIEVED ✨"))
            print(f"{C_YELLOW}[!] Ability combination already mastered!{C_RESET}")

    elif args.subcommand == "learn":
        print(f"\n{C_BOLD}{C_PINK}🧠 INITIATING KIRBY AUTOPOIETIC CURIOSITY LEARNING ({args.count} steps)...{C_RESET}")
        for i in range(args.count):
            learned = engine.run_curiosity_learning_step()
            summary = learned.get("summary", "Processed iteration")
            l_type = learned.get("type", "UNKNOWN")
            print(f"  [{i+1}/{args.count}] {C_CYAN}{l_type:<20}{C_RESET} {C_GREEN}✓{C_RESET} {summary}")
            time.sleep(0.15)
        print(f"\n{C_BOLD}{C_GREEN}✨ LEARNING CYCLE COMPLETE! Kirby's Action Deck expanded & refined! Poyo! 🌸✨{C_RESET}\n")

    elif args.subcommand == "ledger":
        if not LEDGER_FILE.exists():
            print(f"{C_YELLOW}Ledger is empty.{C_RESET}")
            return
        print(f"\n{C_BOLD}{C_CYAN}📜 KIRBY EVOLUTIONARY LEARNING LEDGER (Recent 15 Entries){C_RESET}")
        print(f"{C_DIM}Location: {LEDGER_FILE}{C_RESET}\n")
        with open(LEDGER_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines[-15:]:
            data = json.loads(line.strip())
            ts = data.get("timestamp", "")
            act = data.get("action", "")
            details = data.get("details") or data.get("name") or data.get("event") or ""
            print(f"  {C_DIM}[{ts}]{C_RESET} {C_YELLOW}{act:<28}{C_RESET} {C_WHITE}{details}{C_RESET}")
        print()


if __name__ == "__main__":
    main()
