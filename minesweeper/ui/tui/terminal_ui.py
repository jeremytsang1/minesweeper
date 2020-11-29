from minesweeper.ui.tui.table_printer import TablePrinter


class TerminalUI():
    """Command Line Interface for Minesweeper

    """
    def __init__(self, ):
        self.game = None

    def render_board(self):
        return TablePrinter.makeTable(self.board.get_grid())

    def start_game(self):
        pass
