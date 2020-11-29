from minesweeper.ui.tui.table_printer import TablePrinter


class TerminalUI():
    """Command Line Interface for Minesweeper

    """
    MAX_INT = 1000000
    MAIN_MENU = (
        "1. New Game",
        "2. Quit",
    )
    NEW_GAME_MENU = (
        "1. Easy",
        "2. Medium",
        "3. Hard",
        "4. Custom",
    )
    HEIGHT_PROMPT = "How many rows?"
    WIDTH_PROMPT = "How many cols?"
    BOMB_PROMPT = (
        "\nHow many bombs? (must be in the range "
        "[1 (inclusive) ... {} (exclusive)])"
    )
    GAME_MENU = (
        "1. Open single cell",
        "2. Open all adjacents to a particular cell",
        "3. Quit.",
    )
    ROW_PROMPT = "\nWhich row?"
    COL_PROMPT = "\nWhich col?"

    def __init__(self, ):
        self.game = None

    def render_board(self):
        return TablePrinter.makeTable(self.board.get_grid())

    def start_game(self):
        pass
