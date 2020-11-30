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


if __name__ == '__main__':
    unittest.main()
