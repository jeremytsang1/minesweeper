import unittest
from minesweeper.ui.tui.terminal_ui import TerminalUI
from minesweeper.ui.tui.command_line_grid import CommandLineGrid
from minesweeper.game.board import Board


class TestTerminalUI(unittest.TestCase):
    def setUp(self):
        self.tui = TerminalUI()

    def test_render_board_artificial(self):
        height, width = 10, 10
        self.tui.board = Board(height, width)
        self.tui.coli_grid = CommandLineGrid(height, width)
        actual = (
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "|   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 0 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 1 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 2 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 3 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 4 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 5 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 6 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 7 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 8 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|\n"
            "| 9 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
            "|---+---+---+---+---+---+---+---+---+---+---|"
        )
        expected = self.tui.render_board()
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
