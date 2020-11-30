import unittest
from minesweeper.game.position_util import (
    PositionUtil,
    InvalidComponent,
)


class TestPositionUtil(unittest.TestCase):
    def setUp(self):
        self.pos_util = PositionUtil(10, 10)

    def cmp(self, shape, pos, expected, display=False):
        self.pos_util = PositionUtil(*shape)
        actual = self.pos_util.adj(*pos)
        if display:
            print(f'actual: {actual}')
            print(f'expected: {expected}')
        self.assertEqual(actual, expected)

    def test_negative_components(self):
        with self.assertRaises(InvalidComponent):
            self.pos_util = PositionUtil(-10, -2)

    def test_zero_components(self):
        with self.assertRaises(InvalidComponent):
            self.pos_util = PositionUtil(0, 2)

    def test_adjacent_one_row_left(self):
        shape = (1, 5)
        pos = (0, 0)
        expected = {(0, 1)}
        self.cmp(shape, pos, expected)

    def test_adjacent_one_row_right(self):
        shape = (1, 5)
        pos = (0, 4)
        expected = {(0, 3)}
        self.cmp(shape, pos, expected)

    def test_adjacent_one_row_interior(self):
        shape = (1, 5)
        pos = (0, 1)
        expected = {(0, 0), (0, 2)}
        self.cmp(shape, pos, expected)

    def test_adjacent_one_col_top(self):
        shape = (5, 1)
        pos = (0, 0)
        expected = {(1, 0)}
        self.cmp(shape, pos, expected)

    def test_adjacent_one_col_bottom(self):
        shape = (5, 1)
        pos = (4, 0)
        expected = {(3, 0)}
        self.cmp(shape, pos, expected)

    def test_adjacent_one_col_interior(self):
        shape = (5, 1)
        pos = (1, 0)
        expected = {(0, 0), (2, 0)}
        self.cmp(shape, pos, expected)

    def test_adj_grid_upper_left_corner(self):
        shape = (30, 30)
        pos = (0, 0)
        expected = {(0, 1), (1, 0), (1, 1)}
        self.cmp(shape, pos, expected)

    def test_adj_grid_upper_right_corner(self):
        shape = (30, 30)
        pos = (0, 29)
        expected = {(0, 28), (1, 29), (1, 28)}
        self.cmp(shape, pos, expected)

    def test_adj_grid_lower_left_corner(self):
        shape = (30, 30)
        pos = (29, 0)
        expected = {(28, 0), (29, 1), (28, 1)}
        self.cmp(shape, pos, expected)

    def test_adj_grid_lower_right_corner(self):
        shape = (30, 30)
        pos = (29, 29)
        expected = {(28, 29), (29, 28), (28, 28)}
        self.cmp(shape, pos, expected)

    def test_adj_grid_right_side(self):
        shape = (30, 30)
        pos = ()
        expected = {}
        self.cmp(shape, pos, expected)

    def test_adj_grid_top_side(self):
        shape = (30, 30)
        pos = ()
        expected = {}
        self.cmp(shape, pos, expected)

    def test_adj_grid_left_side(self):
        shape = (30, 30)
        pos = ()
        expected = {}
        self.cmp(shape, pos, expected)

    def test_adj_grid_bottom_side(self):
        shape = (30, 30)
        pos = ()
        expected = {}
        self.cmp(shape, pos, expected)


if __name__ == '__main__':
    unittest.main()
