import unittest
from unittest.mock import patch
from minesweeper.ui.tui.terminal_ui import TUI
from minesweeper.ui.tui.grid_printing.command_line_grid import CommandLineGrid
from minesweeper.game.board import Board

MODULE_NAME = 'tests.ui.tui.test_terminal_ui'

def get_input(text):
    return input(text)

def answer():
    ans = get_input('enter yes or no')
    if ans == 'yes':
        return 'you entered yes'
    if ans == 'no':
        return 'you entered no'


class TestTerminalUI(unittest.TestCase):
    def setUp(self):
        self.tui = TUI()

    @patch(f'{MODULE_NAME}.get_input', return_value='yes')
    def test_answer_yes(self, input):
        self.assertEqual(answer(), 'you entered yes')


    # def test_render_board_artificial(self):
    #     height, width = 10, 10
    #     self.tui.board = Board(height, width)
    #     self.tui.coli_grid = CommandLineGrid(height, width)
    #     actual = (
    #         "|---+---+---+---+---+---+---+---+---+---+---|\n"
    #         "|   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |\n"
    #         "|---+---+---+---+---+---+---+---+---+---+---|\n"
    #         "| 0 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
    #         "|---+---+---+---+---+---+---+---+---+---+---|\n"
    #         "| 1 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
    #         "|---+---+---+---+---+---+---+---+---+---+---|\n"
    #         "| 2 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
    #         "|---+---+---+---+---+---+---+---+---+---+---|\n"
    #         "| 3 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
    #         "|---+---+---+---+---+---+---+---+---+---+---|\n"
    #         "| 4 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
    #         "|---+---+---+---+---+---+---+---+---+---+---|\n"
    #         "| 5 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
    #         "|---+---+---+---+---+---+---+---+---+---+---|\n"
    #         "| 6 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
    #         "|---+---+---+---+---+---+---+---+---+---+---|\n"
    #         "| 7 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
    #         "|---+---+---+---+---+---+---+---+---+---+---|\n"
    #         "| 8 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
    #         "|---+---+---+---+---+---+---+---+---+---+---|\n"
    #         "| 9 | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |\n"
    #         "|---+---+---+---+---+---+---+---+---+---+---|"
    #     )
    #     expected = self.tui.render_board()
    #     self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
