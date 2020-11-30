import unittest
from minesweeper.game.position_util import (
    PositionUtil,
    InvalidComponent,
)


class TestPositionUtil(unittest.TestCase):
    def setUp(self):
        self.pos_util = PositionUtil(10, 10)

    def test_negative_components(self):
        with self.assertRaises(InvalidComponent):
            self.pos_util = PositionUtil(-10, -2)

    def test_zero_components(self):
        with self.assertRaises(InvalidComponent):
            self.pos_util = PositionUtil(0, 2)

    def test_adjacent_one_row_left(self):
        self.pos_util = PositionUtil(1, 5)
        pos = (0, 0)
        expected = {(0, 1)}
        actual = self.pos_util.adj(*pos)
        self.assertEqual(actual, expected)

    def test_adjacent_one_row_right(self):
        self.pos_util = PositionUtil(1, 5)
        pos = (0, 4)
        expected = {(0, 3)}
        actual = self.pos_util.adj(*pos)
        self.assertEqual(actual, expected)

    def test_adjacent_one_row_interior(self):
        self.pos_util = PositionUtil(1, 5)
        pos = (0, 1)
        expected = {(0, 0), (0, 2)}
        actual = self.pos_util.adj(*pos)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
