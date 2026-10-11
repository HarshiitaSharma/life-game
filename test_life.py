"""Unit tests for life.py. Run with: python3 -m unittest -v"""
import unittest

from life import (ALIVE, DEAD, PATTERNS, count_live_cells, empty_grid,
                  grid_from_pattern, next_generation, count_live_neighbors)


def grid_from(rows):
    return [[ALIVE if ch == "#" else DEAD for ch in row] for row in rows]


class TestRules(unittest.TestCase):
    def test_blinker_oscillates_with_period_2(self):
        g = grid_from([".....", "..#..", "..#..", "..#..", "....."])
        g1 = next_generation(g)
        self.assertNotEqual(g, g1)
        self.assertEqual(g, next_generation(g1))

    def test_block_is_still_life(self):
        g = grid_from(["....", ".##.", ".##.", "...."])
        self.assertEqual(g, next_generation(g))

    def test_lonely_cell_dies(self):
        g = grid_from(["...", ".#.", "..."])
        self.assertEqual(count_live_cells(next_generation(g)), 0)

    def test_birth_with_three_neighbors(self):
        g = grid_from(["##.", "#..", "..."])
        self.assertEqual(next_generation(g)[1][1], ALIVE)

    def test_overpopulation(self):
        g = grid_from(["###", "###", "###"])
        self.assertEqual(next_generation(g)[1][1], DEAD)


class TestTorus(unittest.TestCase):
    def test_neighbors_wrap(self):
        g = empty_grid(5, 5)
        g[0][0] = ALIVE
        self.assertEqual(count_live_neighbors(g, 4, 4), 1)

    def test_glider_returns_after_wrapping(self):
        g = grid_from_pattern(8, 8, "glider")
        start = count_live_cells(g)
        for _ in range(32):  # 4 gens per cell moved * 8 cells
            g = next_generation(g)
        self.assertEqual(count_live_cells(g), start)


class TestPatterns(unittest.TestCase):
    def test_all_patterns_place_cells(self):
        for name, cells in PATTERNS.items():
            g = grid_from_pattern(60, 40, name)
            self.assertEqual(count_live_cells(g), len(cells), name)


if __name__ == "__main__":
    unittest.main()
