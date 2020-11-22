import unittest

from minesweeper.ui.tui.command_line_grid import CommandLineGrid

class TestCommandLineGrid(unittest.TestCase):
    def setUp(self):
        self.coli_grid = CommandLineGrid(10, 10)

    def print_cmp(self, actual, expected):
        print(f'actual:\n{actual}')
        print(f'expected:\n{expected}')

    def test_digit_count(self):
        self.assertEqual(CommandLineGrid.digit_count(124), 3)
        self.assertEqual(CommandLineGrid.digit_count(3357395), 7)

    def test_divider(self):
        expected = "|---+---+---+---+---+---+---+---+---+---+---|"
        actual = self.coli_grid.make_divider()
        self.assertEqual(actual, expected)

    def test_empty_row(self):
        expected = "|   |   |   |   |   |   |   |   |   |   |   |"
        actual = self.coli_grid.make_row()
        self.assertEqual(actual, expected)

    def test_col_nums(self, ):
        expected = "|   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |"
        actual = self.coli_grid.make_col_num_row()
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
