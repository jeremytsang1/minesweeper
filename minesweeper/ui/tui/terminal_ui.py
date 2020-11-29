from minesweeper.ui.tui.table_printer import TablePrinter


class TerminalUI():
    """Command Line Interface for Minesweeper

    """
    MAX_INT = 1000000
    MAIN_MENU = (
        "\n1. New Game"
        "\n2. Quit"
    )
    NEW_GAME_MENU = (
        "\n1. Easy"
        "\n2. Medium"
        "\n3. Hard"
        "\n4. Custom"
    )
    HEIGHT_PROMPT = "\nHow many rows?"
    WIDTH_PROMPT = "\nHow many cols?"
    BOMB_PROMPT = (
        "\nHow many bombs? (must be in the range "
        "[1 (inclusive) ... {} (exclusive)])"
    )
    GAME_MENU = (
        "\n1. Open single cell"
        "\n2. Open all adjacents to a particular cell"
        "\n3. Quit."
    )
    ROW_PROMPT = "\nWhich row?"
    COL_PROMPT = "\nWhich col?"

    def __init__(self, ):
        self.game = None

    def render_board(self):
        return TablePrinter.makeTable(self.board.get_grid())

    def start_game(self):
        pass
