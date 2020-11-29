from minesweeper.ui.tui.table_printer import TablePrinter


class TUI():
    """Command Line Interface for Minesweeper

    """
    MAX_INT = 1000000
    PROMPT_APPEARANCE = "\n{}\n> "
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
            2: self.quit_and_end_program
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
        self.make_game_info(10, 10, 10)
        self.display_start_game("EASY")

    def start_medium(self):
        self.make_game_info(16, 16, 40)
        self.display_start_game("MEDIUM")

    def start_hard(self):
        self.make_game_info(16, 30, 99)
        self.display_start_game("HARD")

    def start_custom(self):
        self.make_game_info(*self.read_custom_game_data())
        self.display_start_game("CUSTOM")

    @staticmethod
    def read_custom_game_data():
        height = TUI.read_int(TUI.HEIGHT_PROMPT, 1, TUI.MAX_INT)
        width = TUI.read_int(TUI.WIDTH_PROMPT, 1, TUI.MAX_INT)
        max_bomb_count = height * width
        bomb_count = TUI.read_int(
            TUI.BOMB_PROMPT.format(max_bomb_count),
            min_val=1,
            max_val=max_bomb_count,
        )
        return height, width, bomb_count

    def display_start_game(self, difficulty):
        print(
            "",
            f"Starting {difficulty} game!",
            f"height: {self.height}",
            f" width: {self.width}",
            f" bombs: {self.bomb_count}",
            sep="\n",
        )

    def make_game_info(self, height, width, bomb_count):
        self.height = height
        self.width = width
        self.bomb_count = bomb_count

    @staticmethod
    def quit_and_end_program():
        print(f'\n{TUI.GOODBYE}')

    def get_position_from_user(self):
        row = self.read_int(f"{TUI.ROW_PROMPT}")  # TODO: restrict to max row
        col = self.read_int(f"{TUI.COL_PROMPT}")  # TODO: restrict to max col
        return row, col

    @staticmethod
    def read_menu_option(menu):
        return TUI.read_int(TUI.make_menu_str(menu), 1, len(menu) + 1)

    @staticmethod
    def read_int(msg, min_val=0, max_val=MAX_INT):
        usr_input = None
        while usr_input is None:
            try:
                usr_input = int(input(TUI.PROMPT_APPEARANCE.format(msg)))
                usr_input = TUI.validate_range(usr_input, min_val, max_val)
            except ValueError:
                print("\nPlease enter an integer!")
                usr_input = None
        return usr_input

    @staticmethod
    def validate_range(val, min_val, max_val):
        if val in range(min_val, max_val):
            return val
        else:
            print(
                "\nPlease enter an int in the interval",
                TUI.make_range_string(min_val, max_val)
            )

            return None

    @staticmethod
    def make_range_string(min_val, max_val):
        return f"[{min_val} (inclusive) ... {max_val} (exclusive)]"

    @staticmethod
    def make_menu_str(menu):
        return "\n".join(menu)


if __name__ == '__main__':
    tui = TUI()
