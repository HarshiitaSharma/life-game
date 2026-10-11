# Conway's Game of Life

A tiny, dependency-free Python implementation of Conway's Game of Life that
runs in your terminal, plus a few tools for exploring it.

## Quick start

```bash
python3 life.py                          # random soup
python3 life.py --pattern glider_gun     # classic glider emitter
python3 -m unittest -v                   # run the tests
```

## What's inside

| File | What it does |
|------|--------------|
| `life.py` | The simulation + terminal renderer (toroidal grid) |
| `test_life.py` | Unit tests for the rules, wrapping and patterns |
| `rle.py` | Import/export patterns in the standard RLE format |
| `stats.py` | Headless run that plots population as a sparkline |
| `export_html.py` | Export a run as a shareable, self-contained HTML animation |
| `Makefile` | Shortcuts: `make run`, `make test`, `make gun`, `make stats` |

## The rules

1. A live cell with 2 or 3 live neighbors survives.
2. A dead cell with exactly 3 live neighbors becomes alive.
3. Every other live cell dies.

## Ideas for next steps

- Add more patterns (pulsar, pentadecathlon, Lightweight spaceship)
- Detect when the simulation reaches a stable or periodic state
- Interactive editing mode
- Speed up `next_generation` with a set-of-live-cells approach