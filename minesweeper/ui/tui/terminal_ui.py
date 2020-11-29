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
        "How many bombs? (must be in the range "
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

    def __init__(self):
        self.game = None

    def render_board(self):
        return TablePrinter.makeTable(self.board.get_grid())

    def start_game(self):
        MENU_ACTIONS = {
            1: self.new_game,
            2: self.end_game
        }

        menu_option = self.read_menu_option(self.MAIN_MENU)

        MENU_ACTIONS[menu_option]()

    def new_game(self):
        MENU_ACTIONS = {
            1: self.start_easy,
            2: self.start_medium,
            3: self.start_hard,
            4: self.start_custom,
        }

        menu_option = self.read_menu_option(self.NEW_GAME_MENU)

        MENU_ACTIONS[menu_option]()

    def start_easy(self):
        print("\nStarting EASY game")
        pass

    def start_medium(self):
        print("\nStarting MEDIUM game")
        pass

    def start_hard(self):
        print("\nStarting HARD game")
        pass

    def start_custom(self):
        print("\nStarting CUSTOM game")
        pass

    @staticmethod
    def end_game():
        print(f'\n{TerminalUI.GOODBYE}')

    def get_position_from_user(self):
        row = self.read_int(f"{TerminalUI.ROW_PROMPT}")  # TODO: restrict to max row
        col = self.read_int(f"{TerminalUI.COL_PROMPT}")  # TODO: restrict to max col
        return row, col

    @staticmethod
    def read_menu_option(menu):
        return TerminalUI.read_int(TerminalUI.make_menu_str(menu), 1, len(menu) + 1)

    @staticmethod
    def read_int(msg, min_val=0, max_val=MAX_INT):
        val = None
        while val is None:
            try:
                val = TerminalUI.validate_range(int(input(f"\n{msg}\n> ")), min_val, max_val)
            except ValueError:
                print("\nPlease enter an integer!")
                val = None
        return val

    @staticmethod
    def validate_range(val, min_val, max_val):
        if val in range(min_val, max_val):
            return val
        else:
            print(
                "\nPlease enter an int in the interval",
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
