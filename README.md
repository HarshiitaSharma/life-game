# Conway's Game of Life

A tiny, dependency-free implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) that runs right in your terminal.

Four simple rules, applied to every cell at once each generation, are enough to produce gliders, oscillators, still lifes, and patterns that seem to "live".

```
Generation 42  |  Live cells: 87  |  Ctrl+C to stop
..........................................
.....##...................................
....#..#..................................
.....##.........###.......................
..........................................
```

## Features

- Pure Python 3, standard library only — nothing to install
- Random starts or classic named patterns (glider, blinker, toad, beacon, Gosper glider gun)
- Toroidal grid: patterns that leave one edge reappear on the opposite side
- Adjustable grid size, speed, and starting density
- Live generation counter and population count
- Stops automatically on extinction, or after a set number of generations

## Requirements

- Python 3.6+
- A terminal that supports ANSI escape codes (most do, including macOS Terminal, Linux terminals, Windows Terminal, and VS Code's terminal)

## Quick start

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
python3 life.py
```

Press `Ctrl+C` to stop.

## Usage

```bash
python3 life.py                                    # random starting grid
python3 life.py --pattern glider                   # start with a known pattern
python3 life.py --pattern glider_gun --width 50 --height 30
python3 life.py --width 60 --height 25 --delay 0.05
python3 life.py --density 0.4 --generations 200    # denser start, stop after 200 generations
```

### Options

| Option | Default | Description |
| --- | --- | --- |
| `--width` | `min(70, terminal width - 2)` | Grid width in cells |
| `--height` | `min(30, terminal height - 4)` | Grid height in cells |
| `--delay` | `0.1` | Seconds between generations |
| `--pattern` | *(random)* | Start from a known pattern: `glider`, `blinker`, `toad`, `beacon`, `glider_gun` |
| `--density` | `0.25` | Fraction of cells alive at the start (random starts only) |
| `--generations` | `0` | Stop after N generations (`0` = run until `Ctrl+C` or extinction) |

> **Tip:** The Gosper glider gun is about 36 cells wide, so give it room with `--width 50` or more.

## The rules

Each generation, every cell looks at its eight neighbors:

1. A live cell with 2 or 3 live neighbors **survives**.
2. A dead cell with exactly 3 live neighbors **becomes alive**.
3. A live cell with fewer than 2 live neighbors **dies** (underpopulation).
4. A live cell with more than 3 live neighbors **dies** (overpopulation).

## Built-in patterns

| Name | Type | What it does |
| --- | --- | --- |
| `glider` | Spaceship | Travels diagonally across the grid forever |
| `blinker` | Oscillator | Flips between horizontal and vertical (period 2) |
| `toad` | Oscillator | Two-phase oscillator (period 2) |
| `beacon` | Oscillator | Two blocks that blink at their touching corners (period 2) |
| `glider_gun` | Gun | Gosper glider gun — endlessly emits gliders |

## Adding your own pattern

Patterns are lists of `(row, col)` offsets of live cells in the `PATTERNS` dictionary at the top of `life.py`:

```python
PATTERNS = {
    ...
    "block": [(0, 0), (0, 1), (1, 0), (1, 1)],
}
```

Then run it with `python3 life.py --pattern block`.

## How it works

- `next_generation()` builds a fresh grid each step so all cells update simultaneously.
- `count_live_neighbors()` uses modulo arithmetic to wrap around the edges.
- `render()` uses ANSI escape codes to redraw the grid in place.

