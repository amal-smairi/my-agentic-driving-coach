#!/usr/bin/env python3
"""Generate a synthetic perturbed driver behavior trace for the CSE 598 extension.

Usage:
    python scripts/generate_driver_trace.py --seed 42 --output data/driver/generated_seed_42.txt
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path


def generate_trace(seed: int, length: int = 127) -> list[int]:
    """Generate a valid sequence of driver actions (integers 1-6) using a seeded PRNG.

    The trace models an approaching driver with initial acceleration/cruising (ticks 0-30),
    coasting/intermittent cruising (ticks 30-70), and varying delayed braking attempts
    (ticks 70-127). Seeded noise introduces variance in braking onset and intensity.
    """
    rng = random.Random(seed)
    actions: list[int] = []

    # Phase 1 (0 to 30): Acceleration and cruising
    for _ in range(30):
        # Mostly normal acceleration (3) or cruise (2)
        r = rng.random()
        if r < 0.6:
            actions.append(3)
        elif r < 0.9:
            actions.append(2)
        else:
            actions.append(1)

    # Phase 2 (30 to 70): Coasting / cruise maintaining speed
    for _ in range(40):
        r = rng.random()
        if r < 0.7:
            actions.append(1)  # coasting
        elif r < 0.9:
            actions.append(2)  # cruise
        else:
            actions.append(3)  # occasional late acceleration

    # Phase 3 (70 to 127): Late or inconsistent braking
    # Different seeds cause different delay in braking reaction
    brake_onset = 75 + rng.randint(0, 20)
    for i in range(70, length):
        if i < brake_onset:
            actions.append(1)  # still coasting, ignoring stop sign
        else:
            # Trying to brake (gentle 5 or emergency 6, or coasting 1)
            r = rng.random()
            if r < 0.5:
                actions.append(6)
            elif r < 0.8:
                actions.append(5)
            else:
                actions.append(1)

    return actions


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, required=True, help="RNG seed")
    parser.add_argument("--length", type=int, default=127, help="number of ticks")
    parser.add_argument("--output", type=Path, required=True, help="output file path")
    args = parser.parse_args()

    actions = generate_trace(args.seed, args.length)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        for a in actions:
            f.write(f"{a}\n")

    print(f"Generated {len(actions)} driver actions with seed {args.seed} -> {args.output}")


if __name__ == "__main__":
    main()
