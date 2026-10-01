# Conway's Game of Life

A terminal-based implementation of **Conway's Game of Life**, a cellular automaton where cells evolve automatically according to a set of simple rules.

## Features

- Random starting grid
- Predefined patterns:
  - Glider
  - Blinker
  - Toad
  - Beacon
  - Gosper Glider Gun
- Wrap-around grid edges
- Configurable grid width and height
- Configurable generation delay
- Configurable initial cell density
- Fixed number of generations or continuous execution
- Live-cell counter
- Real-time terminal animation

## Rules

Each cell is either **alive (`#`)** or **dead (`.`)**.

The state of each cell is determined by its neighboring cells:

1. A live cell with 2 or 3 live neighbors survives.
2. A dead cell with exactly 3 live neighbors becomes alive.
3. A live cell with fewer than 2 live neighbors dies due to underpopulation.
4. A live cell with more than 3 live neighbors dies due to overpopulation.

The grid wraps around at the edges, so cells leaving one side reappear on the opposite side.

## Requirements

- Python 3
- No external libraries required

## Usage

Run with a random starting grid:

```bash
python3 life.py
Start with a glider:
python3 life.py --pattern glider
Start the Gosper Glider Gun with a custom grid:
python3 life.py --pattern glider_gun --width 50 --height 30
Run with a custom grid size and delay:
python3 life.py --width 60 --height 25 --delay 0.05
Run for a fixed number of generations:
python3 life.py --generations 100
