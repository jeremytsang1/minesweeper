import unittest
from minesweeper.game.position import (
    Position,
    NegativeCoordsError,
)

class TestPosition(unittest.TestCase):
    def setUp(self):
        self.pos = None

    def test_fail_negative_row(self):
        with self.assertRaises(NegativeCoordsError):
            self.pos = Position(-5, 3050)

    def test_fail_negative_col(self):
        with self.assertRaises(NegativeCoordsError):
            self.pos = Position(3958, -35)

    def test_fail_negative_row_and_col(self):
        with self.assertRaises(NegativeCoordsError):
            self.pos = Position(-124, -32905)

    def test_get_row(self):
        self.pos = Position(3, 8)
        self.assertEqual(self.pos.get_row(), 3)

    def test_get_col(self):
        self.pos = Position(3, 8)
        self.assertEqual(self.pos.get_col(), 8)

    def test_get_coord(self):
        self.pos = Position(3, 8)
        self.assertEqual(self.pos.get_coord(), (3, 8))




if __name__ == '__main__':
    unittest.main()
