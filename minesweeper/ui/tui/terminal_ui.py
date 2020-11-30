from minesweeper.ui.tui.table_printer import TablePrinter
from minesweeper.game.board import Board
from minesweeper.game.game import Game


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
    FIRST_TURN_MENU = (
        "1. Open cell",
        "2. Quit.",
    )
    TURN_MENU = (
        "1. Open cell",
        "2. Flag cell",
        "3. Chord cell (http://www.minesweeper.info/wiki/Chord)",
        "4. Quit.",
    )
    ROW_PROMPT = "\nWhich row?"
    COL_PROMPT = "\nWhich col?"
    GOODBYE = "Goodbye!"

    def __init__(self):
        self.reset_attributes()

    def reset_attributes(self):
        self.game = None
        self.height = None
        self.width = None
        self.bomb_count = None
        self.turn = None

    # -------------------------------------------------------------------------
    # Main menu functions

    def start_game(self):
        MENU_ACTIONS = {
            1: self.new_game,
            2: self.quit_and_end_program
        }
        menu_option = self.read_menu_option(self.MAIN_MENU)
        MENU_ACTIONS[menu_option]()

    # -------------------------------------------------------------------------
    # New game menu functions

    def new_game(self):
        self.reset_attributes()

        MENU_ACTIONS = {
            1: self.start_easy,
            2: self.start_medium,
            3: self.start_hard,
            4: self.start_custom,
        }
        menu_option = self.read_menu_option(self.NEW_GAME_MENU)
        MENU_ACTIONS[menu_option]()

        self.turn = 0
        self.take_first_turn()

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

    def make_game_info(self, height, width, bomb_count):
        self.height = height
        self.width = width
        self.bomb_count = bomb_count

    def display_start_game(self, difficulty):
        print(
            "",
            f"Starting {difficulty} game!",
            f"height: {self.height}",
            f" width: {self.width}",
            f" bombs: {self.bomb_count}",
            sep="\n",
        )

    # -----------------------------------------------------------------------------
    # First turn menu functions

    def take_first_turn(self):
        MENU_ACTION = {
            1: self.open_first_cell,
            2: self.quit_and_end_program,
        }
        assert self.game is None
        assert self.turn == 0

        self.print_turn()
        self.display_board_to_user()

        menu_option = self.read_menu_option(TUI.FIRST_TURN_MENU)
        MENU_ACTION[menu_option]()

    def open_first_cell(self):
        pos = self.get_position_from_user()
        self.game = Game(self.height, self.width, self.bomb_count, *pos)
        self.turn += 1
        self.take_turn()

    # -------------------------------------------------------------------------
    # Turn menu functions

    def take_turn(self):
        MENU_ACTIONS = {
            1: self.open_cell,
            2: self.flag_cell,
            3: self.chord_cell,
            4: self.quit_and_end_program,
        }
        self.print_turn()
        self.display_board_to_user()

        menu_option = self.read_menu_option(self.TURN_MENU)
        valid_move = MENU_ACTIONS[menu_option]()

        if valid_move is not None:
            self.process_move(valid_move)
        else:
            pass  # Quit the program.

    def print_turn(self):
        print(f"\nTurns taken: {self.turn}")

    def display_board_to_user(self):
        if self.turn == 0 and self.game is None:
            # Need the user to make a move before initializing a real board.
            self.print_dummy_board()
        elif self.turn != 0 and self.game is not None:
            self.print_real_board()
            pass
        elif self.turn == 0 and self.game is not None:
            raise DidNotErasePreviousGameError
        else:  # self.turn != 0  and self.game is None
            raise NoGameInstance

    def print_dummy_board(self):
        print('\nprint_dummy_board()')
        dummy_board = Board([[False for _ in range(self.width)]
                             for _ in range(self.height)])
        print(TablePrinter.makeTable(dummy_board.get_grid()))

    def print_real_board(self):
        print('\nprint_real_board()')
        print(TablePrinter.makeTable(self.game.get_grid()))

    def open_cell(self):
        print("\nOpening!")
        pass

    def flag_cell(self):
        valid_move = True
        return valid_move

    def chord_cell(self):
        print("\nChording!")
        pass

    def process_move(self, valid_move):
        if valid_move:
            self.turn += 1
            if True in self.game.check_end_game():
                self.showEndGameResults(self.game.check_end_game())
                self.start_game()  # Go back to the main menu.
            else:
                self.take_turn()
        else:
            assert type(valid_move.get_message()) == str
            print("", valid_move.get_message(), sep="\n")
            self.take_turn()

    # -------------------------------------------------------------------------
    # End game and quitting functions

    @staticmethod
    def quit_and_end_program():
        print(f'\n{TUI.GOODBYE}')
        return None

    # -------------------------------------------------------------------------
    # Input functions

    def get_position_from_user(self):
        """Assumes a game is currently running."""
        row = self.read_int(f"{TUI.ROW_PROMPT}", 0, self.height)
        col = self.read_int(f"{TUI.COL_PROMPT}", 0, self.width)
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
        """Use to concatenate menu iterables into single string."""
        return "\n".join(menu)


class TUIError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DidNotErasePreviousGameError(TUIError):
    def __init__(self, turn):
        super().__init__("It's turn 0 but no game still using previous game!")


class NoGameInstance(TUIError):
    def __init__(self, turn):
        super().__init__("It's not turn 0 but game has not been created!")


if __name__ == '__main__':
    tui = TUI()
