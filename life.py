"""
Conway's Game of Life — a cellular automaton that runs itself.

Four simple rules, applied to every cell on a grid simultaneously each
generation, are enough to produce gliders, oscillators, still lifes, and
patterns that seem to "live":

  1. A live cell with 2 or 3 live neighbors survives.
  2. A dead cell with exactly 3 live neighbors becomes alive.
  3. Any live cell with fewer than 2 live neighbors dies (underpopulation).
  4. Any live cell with more than 3 live neighbors dies (overpopulation).

The grid wraps around at the edges (a torus), so patterns that drift off
one side reappear on the other.

Run with:
    python3 life.py                     # random starting grid
    python3 life.py --pattern glider    # start with a known pattern
    python3 life.py --pattern glider_gun --width 50 --height 30
    python3 life.py --width 60 --height 25 --delay 0.05
"""

import argparse
import os
import random
import shutil
import sys
import time

ALIVE = "#"
DEAD = "."

# A few well-known patterns, given as (row, col) offsets of live cells
# relative to a top-left anchor point.
PATTERNS = {
    "glider": [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
    "blinker": [(1, 0), (1, 1), (1, 2)],
    "toad": [(1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2)],
    "beacon": [(0, 0), (0, 1), (1, 0), (1, 1), (2, 2), (2, 3), (3, 2), (3, 3)],
    # Gosper glider gun — the classic pattern that endlessly emits gliders
    "glider_gun": [
        (5, 1), (5, 2), (6, 1), (6, 2),
        (3, 13), (3, 14), (4, 12), (4, 16), (5, 11), (5, 17), (6, 11), (6, 15),
        (6, 17), (6, 18), (7, 11), (7, 17), (8, 12), (8, 16), (9, 13), (9, 14),
        (1, 25), (2, 23), (2, 25), (3, 21), (3, 22), (4, 21), (4, 22), (5, 21),
        (5, 22), (6, 23), (6, 25), (7, 25),
        (3, 35), (3, 36), (4, 35), (4, 36),
    ],
}


def empty_grid(width, height):
    return [[DEAD] * width for _ in range(height)]


def random_grid(width, height, density=0.25):
    return [
        [ALIVE if random.random() < density else DEAD for _ in range(width)]
        for _ in range(height)
    ]


def grid_from_pattern(width, height, pattern_name):
    grid = empty_grid(width, height)
    offsets = PATTERNS[pattern_name]
    anchor_row = max(1, height // 4)
    anchor_col = max(1, width // 4)
    for dr, dc in offsets:
        r, c = anchor_row + dr, anchor_col + dc
        if 0 <= r < height and 0 <= c < width:
            grid[r][c] = ALIVE
    return grid


def count_live_neighbors(grid, row, col):
    height = len(grid)
    width = len(grid[0])
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            # wrap around edges (toroidal grid)
            r = (row + dr) % height
            c = (col + dc) % width
            if grid[r][c] == ALIVE:
                count += 1
    return count


def next_generation(grid):
    height = len(grid)
    width = len(grid[0])
    new_grid = empty_grid(width, height)

    for r in range(height):
        for c in range(width):
            neighbors = count_live_neighbors(grid, r, c)
            alive = grid[r][c] == ALIVE

            if alive and neighbors in (2, 3):
                new_grid[r][c] = ALIVE
            elif not alive and neighbors == 3:
                new_grid[r][c] = ALIVE
            else:
                new_grid[r][c] = DEAD

    return new_grid


def count_live_cells(grid):
    return sum(row.count(ALIVE) for row in grid)


def render(grid, generation, live_count):
    lines = ["".join(row) for row in grid]
    header = f"Generation {generation}  |  Live cells: {live_count}  |  Ctrl+C to stop"
    sys.stdout.write("\x1b[H\x1b[J")  # move cursor home, clear screen
    sys.stdout.write(header + "\n")
    sys.stdout.write("\n".join(lines) + "\n")
    sys.stdout.flush()


def parse_args():
    term_size = shutil.get_terminal_size(fallback=(80, 24))
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument("--width", type=int, default=min(70, term_size.columns - 2),
                         help="Grid width in cells")
    parser.add_argument("--height", type=int, default=min(30, term_size.lines - 4),
                         help="Grid height in cells")
    parser.add_argument("--delay", type=float, default=0.1,
                         help="Seconds between generations")
    parser.add_argument("--pattern", choices=list(PATTERNS.keys()),
                         help="Start from a known pattern instead of random noise")
    parser.add_argument("--density", type=float, default=0.25,
                         help="Fraction of cells alive initially, when using random start")
    parser.add_argument("--generations", type=int, default=0,
                         help="Stop after N generations (0 = run until Ctrl+C or extinction)")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.pattern:
        grid = grid_from_pattern(args.width, args.height, args.pattern)
    else:
        grid = random_grid(args.width, args.height, args.density)

    generation = 0
    try:
        while True:
            live_count = count_live_cells(grid)
            render(grid, generation, live_count)

            if live_count == 0:
                print("\nEverything has died out.")
                break
            if args.generations and generation >= args.generations:
                break

            time.sleep(args.delay)
            grid = next_generation(grid)
            generation += 1
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
