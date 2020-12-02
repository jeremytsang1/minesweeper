import unittest
from minesweeper.game.game import (
    Game,
)


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = None

    # -------------------------------------------------------------------------

    def test_negative_row(self):
        with self.assertRaises(ValueError):
            self.game = Game(-5, 24)

    def test_negative_col(self):
        with self.assertRaises(ValueError):
            self.game = Game(35, -5)

    def test_negative_row_and_col(self):
        with self.assertRaises(ValueError):
            self.game = Game(-35, -5)


if __name__ == '__main__':
    unittest.main()
