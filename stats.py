"""
Run a headless simulation and plot population over time as a sparkline.

    python3 stats.py                      # random 60x30 for 300 generations
    python3 stats.py --pattern glider_gun --generations 500
"""
import argparse

from life import (PATTERNS, count_live_cells, grid_from_pattern, next_generation,
                  random_grid)

BARS = "▁▂▃▄▅▆▇█"


def sparkline(values, width=70):
    step = max(1, len(values) // width)
    sampled = values[::step]
    lo, hi = min(sampled), max(sampled)
    span = (hi - lo) or 1
    return "".join(BARS[int((v - lo) / span * (len(BARS) - 1))] for v in sampled)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--width", type=int, default=60)
    p.add_argument("--height", type=int, default=30)
    p.add_argument("--generations", type=int, default=300)
    p.add_argument("--pattern", choices=list(PATTERNS))
    p.add_argument("--seed", type=int)
    a = p.parse_args()

    if a.seed is not None:
        import random
        random.seed(a.seed)
    g = (grid_from_pattern(a.width, a.height, a.pattern) if a.pattern
         else random_grid(a.width, a.height))
    history = []
    for _ in range(a.generations + 1):
        history.append(count_live_cells(g))
        g = next_generation(g)

    print(sparkline(history))
    print(f"start={history[0]}  end={history[-1]}  "
          f"min={min(history)}  max={max(history)}  "
          f"peak at gen {history.index(max(history))}")


if __name__ == "__main__":
    main()
