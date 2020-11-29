import unittest
from minesweeper.game.board import (
    Board,
    JaggedMinePositionsError,
)
from minesweeper.game.cell import (
    Cell
)


class TestBoard(unittest.TestCase):
    DEFAULT_SHAPE = (10, 10)
    DEFAULT_HEIGHT = DEFAULT_SHAPE[0]
    DEFAULT_WIDTH = DEFAULT_SHAPE[1]

    def setUp(self):
        self.bombs = self.create_all_bombs(self.DEFAULT_HEIGHT,
                                           self.DEFAULT_WIDTH)
        self.board = Board(self.bombs)

    def check_cell_predicate(self, predicate):
        grid = self.board.get_grid()
        for row in grid:
            for cell in row:
                self.assertTrue(predicate(cell))

    def create_all_bombs(self, height, width):
        return [[True for _ in range(height)] for _ in range(width)]

    # -------------------------------------------------------------------------

    def test_initial_shape(self):
        self.board = Board(self.bombs)
        grid = self.board.get_grid()
        self.assertEqual(len(grid), self.DEFAULT_HEIGHT)
        self.assertEqual(len(grid[0]), self.DEFAULT_WIDTH)
        self.assertEqual(self.board.get_height(), self.DEFAULT_HEIGHT)
        self.assertEqual(self.board.get_width(), self.DEFAULT_WIDTH)

    def test_initial_grid_types(self):
        self.bombs = self.create_all_bombs(32, 48)
        self.board = Board(self.bombs)
        self.check_cell_predicate(lambda cell: type(cell) == Cell)

    def test_initial_cell_appearance(self):
        self.bombs = self.create_all_bombs(35, 67)
        self.board = Board(self.bombs)
        self.check_cell_predicate(
            lambda cell: cell.get_appearance() == Cell.Appearance.UNOPENED
        )

    def test_repr_10_10(self):
        expected = (
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?"
        )
        self.assertEqual(repr(self.board), expected)

    def test_repr_1_1(self):
        self.bombs = self.create_all_bombs(1, 1)
        self.board = Board(self.bombs)
        expected = (
            "?"
        )
        self.assertEqual(repr(self.board), expected)


if __name__ == '__main__':
    unittest.main()
