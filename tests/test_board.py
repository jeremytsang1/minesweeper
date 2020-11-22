import unittest
from minesweeper.game.board import (
    Board,
    BoardNegativeDimsError,
)
from minesweeper.game.cell import (
    Cell
)


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(10, 10)

    def check_cell_predicate(self, predicate):
        grid = self.board.get_grid()
        for row in grid:
            for cell in row:
                self.assertTrue(predicate(cell))
    # -------------------------------------------------------------------------

    def test_negative_row(self):
        with self.assertRaises(BoardNegativeDimsError):
            self.board = Board(-5, 24)

    def test_negative_col(self):
        with self.assertRaises(BoardNegativeDimsError):
            self.board = Board(35, -5)

    def test_negative_row_and_col(self):
        with self.assertRaises(BoardNegativeDimsError):
            self.board = Board(-35, -5)

    def test_initial_shape(self):
        self.board = Board(39, 23)
        grid = self.board.get_grid()
        self.assertEqual(len(grid), 39)
        self.assertEqual(len(grid[0]), 23)
        self.assertEqual(self.board.get_height(), 39)
        self.assertEqual(self.board.get_width(), 23)

    def test_initial_grid_types(self):
        height, width = 22, 49
        self.board = Board(height, width)
        self.check_cell_predicate(lambda cell: type(cell) == Cell)

    def test_initial_cell_appearance(self):
        height, width = 35, 67
        self.board = Board(height, width)
        self.check_cell_predicate(
            lambda cell: cell.get_appearance() == Cell.Appearance.UNOPENED
        )


if __name__ == '__main__':
    unittest.main()
