from minesweeper.ui.tui.menus.menu import Menu
from minesweeper.ui.tui.menus.action_menu import ActionMenu
from minesweeper.ui.tui.io import IO
from minesweeper.ui.tui.move_message import MoveMessage
from minesweeper.ui.tui.grid_printing.table_printer import TablePrinter
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
    MAIN_MENU_DESCRIPTIONS = (
        "1. New game",
        "2. Quit",
    )
    NEW_GAME_MENU_DESCRIPTIONS = (
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
    FIRST_TURN_MENU_DESCRIPTIONS = (
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
        self.difficulty = Difficulty()
        self.game = None

        # --------------------
        # Menu attributes (listed in reverse order of when they are called)

        self.turn_menu = None  # Not initialized till self.game is initialized.

        self.first_turn_menu = ActionMenu(
            self.FIRST_TURN_MENU_DESCRIPTIONS,
            (self.open_first_cell,
             self.quit_and_end_program),
        )

        self.new_game_menu = ActionMenu(
            self.NEW_GAME_MENU_DESCRIPTIONS,
            [self.choose_level(level) for level in Difficulty.get_levels()],
        )

        # Must be initialized after self.new_game_menu since it's action is
        # dependent on said attribute's existence.
        self.main_menu = ActionMenu(
            self.MAIN_MENU_DESCRIPTIONS,
            (self.new_game_menu.run_action_for_user_option,
             self.quit_and_end_program),
        )

    # -------------------------------------------------------------------------
    # Main menu functions

    def start(self):
        self.main_menu.run_action_for_user_option()

    # -------------------------------------------------------------------------
    # New game menu functions

    def choose_level(self, level):

        def difficulty_callable():
            is_preset = self.difficulty.set_difficulty(level)

            if not is_preset:
                self.difficulty.set_specs(*self.read_custom_specs())

            self.display_start_game()
            self.display_board_to_user()

            self.first_turn_menu.run_action_for_user_option()

        return difficulty_callable

    @staticmethod
    def read_custom_specs():
        height = IO.read_int(TUI.HEIGHT_PROMPT, 1, TUI.MAX_INT)
        min_cols = 1 if height != 1 else 2  # prevent 1x1 grid
        width = IO.read_int(TUI.WIDTH_PROMPT, min_cols, TUI.MAX_INT)
        max_bomb_count = height * width
        bomb_count = IO.read_int(
            TUI.BOMB_PROMPT.format(max_bomb_count),
            min_val=1,
            max_val=max_bomb_count,
        )
        return height, width, bomb_count

    def display_start_game(self):
        print(
            "",
            f"Starting {self.difficulty.get_current_level()} game!",
            f"height: {self.difficulty.get_rows()}",
            f" width: {self.difficulty.get_cols()}",
            f" bombs: {self.difficulty.get_bomb_count()}",
            sep="\n",
        )

    # -----------------------------------------------------------------------------
    # First turn menu functions

    def open_first_cell(self):
        pos = self.get_position_from_user()
        self.game = Game(*self.difficulty.get_diff_specs(), *pos)

        self.turn_menu = ActionMenu(
            self.TURN_MENU_DESCRIPTIONS,
            (*(self.take_turn(action) for action in self.game.get_actions()),
             self.quit_and_end_program),
        )
        self.display_board_to_user()
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
        dummy_board = Board([[False for _ in range(self.difficulty.get_cols())]
                             for _ in range(self.difficulty.get_rows())])
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
            self.start()
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
        row = IO.read_int(TUI.ROW_PROMPT, 0, self.difficulty.get_rows())
        col = IO.read_int(TUI.COL_PROMPT, 0, self.difficulty.get_cols())
        return row, col


if __name__ == '__main__':
    tui = TUI()
    tui.start()
