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
    GOODBYE = "Goodbye!"

    def __init__(self, ):
        self.game = None

    def render_board(self):
        return TablePrinter.makeTable(self.board.get_grid())

    def start_game(self):
        pass

    @staticmethod
    def read_int(msg, min_val=0, max_val=MAX_INT):
        try:
            return TerminalUI.validate_range(int(input(f"\n{msg}\n> ")), min_val, max_val)
        except ValueError:
            print("Please enter an integer!")
            return None

    @staticmethod
    def validate_range(val, min_val, max_val):
        if val in range(min_val, max_val):
            return val
        else:
            print(
                "Please enter an int in the interval",
                TerminalUI.make_range_string(min_val, max_val)
            )

            return None

    @staticmethod
    def make_range_string(min_val, max_val):
        return f"[{min_val} (inclusive) ... {max_val} (exclusive)]"

    @staticmethod
    def make_menu_str(menu):
        return "\n".join(menu)


if __name__ == '__main__':
    tui = TerminalUI()
