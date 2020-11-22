import unittest
from minesweeper.ui.tui.TerminalUI import TerminalUI
from minesweeper.game.board import Board


class TestTerminalUI(unittest.TestCase):
    def setUp(self):
        self.board = Board(10, 10)
        self.tui = TerminalUI(self.board)
        pass

    def test_digit_count(self):
        self.assertEqual(TerminalUI.digit_count(124), 3)
        self.assertEqual(TerminalUI.digit_count(3357395), 7)

    def test_divider(self):
        expected = "|---+---+---+---+---+---+---+---+---+---+---|"
        self.assertEqual(self.tui.make_divider(), expected)

    def test_empty_row(self):
        print(79 * "-")
        print(self.tui.make_row([''] + [i for i in range(10)]))


    def test_col_nums(self, ):
        expected = (
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "|   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|"
        )

if __name__ == '__main__':
    unittest.main()
