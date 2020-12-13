from minesweeper.ui.tui.menu import Menu
from minesweeper.ui.tui.action_menu import ActionMenu
from minesweeper.ui.tui.io import IO
from minesweeper.ui.tui.terminal_ui_move_message import MoveMessage
from minesweeper.ui.tui.table_printer import TablePrinter
from minesweeper.ui.tui.art import happy, dead
from minesweeper.game.board import Board
from minesweeper.game.game import Game
from minesweeper.game.move import Move
from minesweeper.game.difficulty import Difficulty


class TUI():
    """Command Line Interface for Minesweeper

    """
    MAX_INT = 1000000
    PROMPT_APPEARANCE = "\n{}\n> "
    MAIN_MENU = (
        "1. New game",
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
        "2. Quit",
    )
    TURN_MENU_DESCRIPTIONS = (
        "1. Open cell",
        "2. Toggle flag",
        "3. Chord cell (http://www.minesweeper.info/wiki/Chord)",
        "4. Quit",
    )
    ROW_PROMPT = f"\nWhich row?{Menu.PROMPT_CHAR}"
    COL_PROMPT = f"\nWhich col?{Menu.PROMPT_CHAR}"
    WON_MSG = f"\nYOU WIN!{happy()}"
    LOSS_MSG = f"\nYOU DIED!{dead()}"
    GOODBYE = "\nGoodbye!"

    def __init__(self):
        self.reset_attributes()
        self.turn_menu = None

    def reset_attributes(self):
        self.game = None
        self.height = None
        self.width = None
        self.bomb_count = None

    # -------------------------------------------------------------------------
    # Main menu functions

    def run_main_menu(self):
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
        min_cols = 1 if height != 1 else 2  # prevent 1x1 grid
        width = TUI.read_int(TUI.WIDTH_PROMPT, min_cols, TUI.MAX_INT)
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

        self.display_board_to_user()

        menu_option = self.read_menu_option(TUI.FIRST_TURN_MENU)
        MENU_ACTION[menu_option]()

    def open_first_cell(self):
        pos = self.get_position_from_user()
        self.game = Game(self.height, self.width, self.bomb_count, *pos)

        self.turn_menu = ActionMenu(
            self.TURN_MENU_DESCRIPTIONS,
            (*(self.take_turn(action) for action in self.game.get_actions()),
             self.quit_and_end_program),
        )
        self.process_move(self.game.open_cell(*pos))  # enact first turn

    # -------------------------------------------------------------------------
    # Turn menu functions

    def print_turn(self):
        turns_taken = 0 if self.game is None else self.game.get_turn()
        print(f"\n(Legal) Turns taken: {turns_taken}")

    def display_board_to_user(self):
        self.print_turn()
        if self.game is None:
            # Need the user to make a move before initializing a real board.
            self.print_dummy_board()
        else:
            self.print_real_board()

    def print_dummy_board(self):
        """Print a board with all unopened cells.

        Use a non-live board since don't want to create a game till the user
        clicks to avoid them immediately dying by clicking a mine (Game will
        lay the mines considering every cell except for the one the user
        clicks.
        """
        dummy_board = Board([[False for _ in range(self.width)]
                             for _ in range(self.height)])
        print(TablePrinter.makeTable(dummy_board.get_grid()))

    def print_real_board(self):
        print(TablePrinter.makeTable(self.game.get_grid()))

    def take_turn(self, player_action):

        def perform_player_action():
            pos = self.get_position_from_user()
            move = player_action(*pos)   # Returns a move
            self.process_move(move)

        return perform_player_action

    def process_move(self, move):
        assert type(move) == Move
        if move.is_valid():
            self.process_valid_move()
        else:
            print("Illegal move!")
            print(MoveMessage.MOVE_MSG[move.get_reason_turn_is_invalid()])
            self.display_board_to_user()
            self.turn_menu.run_action_for_user_option()

    def process_valid_move(self):
        won, loss = self.game.check_end_game()
        if won or loss:  # Can't both win and lose.
            self.showEndGameResults(won, loss)
            self.print_real_board()
            self.run_main_menu()
        else:
            self.display_board_to_user()
            self.turn_menu.run_action_for_user_option()

    # -------------------------------------------------------------------------
    # End game and quitting functions

    def showEndGameResults(self, won, loss):
        print(TUI.WON_MSG if won else TUI.LOSS_MSG)

    @staticmethod
    def quit_and_end_program():
        print(f'{TUI.GOODBYE}')
        return None

    # -------------------------------------------------------------------------
    # Input functions

    def get_position_from_user(self):
        """Assumes a game is currently running."""
        row = IO.read_int(f"{TUI.ROW_PROMPT}", 0, self.height)
        col = IO.read_int(f"{TUI.COL_PROMPT}", 0, self.width)
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


if __name__ == '__main__':
    tui = TUI()
    tui.run_main_menu()
