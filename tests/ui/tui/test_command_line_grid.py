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

    def test_col_nums(self):
        expected = "|   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |"
        actual = self.coli_grid.make_col_num_row()
        self.assertEqual(actual, expected)

    def test_letters(self):
        expected = "|   | a | b | c | d | e | f | g | h | i | j |"
        actual = self.coli_grid.make_row(
            [''] + ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        )
        self.assertEqual(actual, expected)

    def test_itr_2d_kronecker_delta_diagonal_matrix(self):
        h = range(self.coli_grid.HEIGHT)
        w = range(self.coli_grid.WIDTH)
        itr_2d = [[1 if i == j else 0 for j in w] for i in h]
        actual = self.coli_grid.make_table_from_itr_2d(itr_2d)
        expected = (
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "|   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 3 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 5 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 6 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|"
        )
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
