#!/usr/bin/env python3
"""
🔮 Oracle of Poyo & Kirby 20Q Wisdom Genie (kirby_oracle.py)
================================================================================
Interactive ASCII wisdom genie where Kirby ( ^-^ ) answers questions, guesses
what concept you are thinking of through binary triage, and dispenses cosmic poyo advice.
================================================================================
"""

import sys
import time
import random
import argparse

PINK = "\033[38;5;205m"
CYAN = "\033[38;5;81m"
YELLOW = "\033[38;5;220m"
GREEN = "\033[38;5;120m"
WHITE = "\033[38;5;255m"
PURPLE = "\033[38;5;141m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

FACES = {
    "happy": "( ^-^ )",
    "excited": "( >o< )",
    "thinking": "( u.u )",
    "serious": "( ಠ ʖ̯ ಠ )",
    "surprised": "( O_O )",
    "victory": "☆彡(>'-')>",
    "love": "( ♥_♥ )",
    "sparkle": "✨( 'v' )✨"
}

ORACLE_ANSWERS = [
    ("Yes! The warp stars align in your favor, poyo!", "happy"),
    ("Signs point to pure copper airflow! Absolutely, poyo!", "excited"),
    ("Poyo... the stars are fuzzy right now. Ask again after a nap!", "thinking"),
    ("Inhale the doubts, exhale the certainty! Yes, poyo!", "victory"),
    ("The Ace Kirby says: proceed with caution and verify your invariants.", "serious"),
    ("Zero packet drop guaranteed! It is decidedly so, poyo!", "sparkle"),
    ("My tomato sensor detects positive energy! Yes!", "love"),
    ("No, poyo. A rogue glitch lurks on that path.", "serious"),
    ("Outlook bright as the celestial sanctuary! Poyo!", "happy"),
    ("Concentrate and ask again while offering a star shard!", "thinking")
]

CONCEPT_TREE = {
    "question": "Is it related to hardware or physical devices?",
    "yes": {
        "question": "Is it a mobile device powered by Tensor G4?",
        "yes": {
            "question": "Does it have 16GB RAM and run Android 16 Terminal AVF?",
            "yes": "Google Pixel 9 Pro XL! (The mother ship!)",
            "no": "A Tensor Edge device or Coral TPU accelerator!"
        },
        "no": {
            "question": "Does it have copper fins spinning at 4500 RPM?",
            "yes": "Wooshie & Shooshie! The dual-fan workstation cooling core!",
            "no": "Windows 11 Workstation Laptop ('Lappy') or host desktop!"
        }
    },
    "no": {
        "question": "Is it a pink, round, cheerful hero who loves eating stars?",
        "yes": {
            "question": "Does this hero wear a top hat or hold a paintbrush?",
            "yes": "Magician / Easel Painter Kirby at the Studio Nook!",
            "no": "Classic Kirby riding a Warp Star across the terminal!"
        },
        "no": {
            "question": "Is it a network protocol or mesh architecture?",
            "yes": {
                "question": "Does it connect Pixel, Windows, and Debian on 100.x.y.z?",
                "yes": "Tailscale Thrice Over Mesh Nexus!",
                "no": "VirtioFS shared storage or WireGuard tunnel!"
            },
            "no": {
                "question": "Is it an artistic or poetic composition?",
                "yes": "An autonomous ASCII Micro-Gem from Kirby Studio!",
                "no": "The universal Day-0 Mesh Watercooler Bus!"
            }
        }
    }
}

def ask_oracle(question=None):
    print(f"\n{BOLD}{PINK}🔮 THE ORACLE OF POYO DISPENSES COSMIC WISDOM{RESET}")
    print(f"{PINK}──────────────────────────────────────────────────{RESET}")
    
    if not question:
        question = input(f"{CYAN}What is your question for the Oracle? > {RESET}").strip()
    
    if not question:
        question = "What should I build today?"

    print(f"\n{DIM}Asking the Oracle: \"{question}\"...{RESET}")
    time.sleep(0.6)
    print(f"{YELLOW}Kirby closes his eyes and meditates on the starlight substrate... ( u.u ){RESET}")
    time.sleep(0.8)

    ans, mood = random.choice(ORACLE_ANSWERS)
    face = FACES.get(mood, "( ^-^ )")

    print(f"\n{BOLD}{GREEN}{face} KIRBY SAYS:{RESET}")
    print(f"{BOLD}{WHITE}  \"{ans}\"{RESET}\n")

def play_20q():
    print(f"\n{BOLD}{CYAN}🧙 KIRBY'S REVERSE 20Q INTENT GENIE{RESET}")
    print(f"{CYAN}──────────────────────────────────────────────────{RESET}")
    print(f"{WHITE}Think of a concept in the AntiGravity / Pixel / Kirby universe!{RESET}")
    print(f"{DIM}(Kirby will ask binary questions to guess your thought){RESET}\n")

    node = CONCEPT_TREE
    while isinstance(node, dict):
        q = node["question"]
        ans = ""
        while ans not in ("y", "n", "yes", "no"):
            ans = input(f"{YELLOW}Kirby asks {FACES['thinking']}: {q} [y/n] > {RESET}").strip().lower()
            if ans in ("q", "quit", "exit"):
                print(f"{PINK}Kirby waves goodbye! Poyo! (>'-')>{RESET}\n")
                return

        choice = "yes" if ans in ("y", "yes") else "no"
        node = node[choice]

    # Guessed!
    time.sleep(0.4)
    print(f"\n{BOLD}{PINK}{FACES['excited']} AHA! POYO! Kirby guesses:{RESET}")
    print(f"{BOLD}{GREEN}  ✨✨✨ {node} ✨✨✨{RESET}\n")

def main():
    parser = argparse.ArgumentParser(description="Oracle of Poyo & Kirby 20Q Genie")
    parser.add_argument("mode", nargs="?", default="ask", choices=["ask", "20q", "wisdom"], help="Activity mode")
    parser.add_argument("question", nargs="?", default=None, help="Question for the oracle")

    args = parser.parse_args()

    if args.mode == "ask" or args.mode == "wisdom":
        ask_oracle(args.question)
    elif args.mode == "20q":
        play_20q()

if __name__ == "__main__":
    main()
