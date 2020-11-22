from minesweeper.ui.tui.command_line_grid import CommandLineGrid


class TerminalUI():
    """Command Line Interface for Minesweeper

    """
    def __init__(self, ):
        self.board = None
        self.coli_grid = None

    def render_board(self):
        return self.coli_grid.make_table_from_2d_itr(self.board.get_grid())

    def start_game(self):
        pass
