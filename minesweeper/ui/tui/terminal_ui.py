from minesweeper.ui.tui.menus.menu import Menu
from minesweeper.ui.tui.menus.action_menu import ActionMenu
from minesweeper.ui.tui.io import IO
from minesweeper.ui.tui.move_message import MoveMessage
from minesweeper.ui.tui.grid_printing.table_printer import TablePrinter
from minesweeper.ui.tui.ascii_art import AsciiArt
from minesweeper.game.game import Game
from minesweeper.game.move import Move
from minesweeper.game.difficulty import Difficulty
from minesweeper.game.cell import Cell


class TUI():
    """Command Line Interface for Minesweeper

    """
    MAX_INT = 1000000

    MAIN_MENU_DESCRIPTIONS = (
        "New game",
        "Quit",
    )

    NEW_GAME_MENU_DESCRIPTIONS = (
        "Easy",
        "Medium",
        "Hard",
        "Custom",
    )
    HEIGHT_PROMPT = "How many rows?"
    WIDTH_PROMPT = "How many cols?"
    BOMB_PROMPT = (
        "How many bombs? (must be in the range "
        "[1 (inclusive) ... {} (exclusive)])"
    )

    FIRST_TURN_MENU_DESCRIPTIONS = (
        "Open cell",
        "Quit",
    )

    TURN_MENU_DESCRIPTIONS = (
        "Open cell",
        "Toggle flag",
        "Chord cell (http://www.minesweeper.info/wiki/Chord)",
        "Quit",
    )

    ROW_PROMPT = f"\nWhich row?{Menu.PROMPT_CHAR}"
    COL_PROMPT = f"\nWhich col?{Menu.PROMPT_CHAR}"

    WON_MSG = f"\nYOU WIN!{AsciiArt.HAPPY}"
    LOSS_MSG = f"\nYOU DIED!{AsciiArt.DEAD}"

    GOODBYE = "\nGoodbye!"

    APPEARANCES = {
        Cell.Appearance.FLAG: 'F',
        Cell.Appearance.EMPTY: ' ',
        Cell.Appearance.UNOPENED: '?',
        Cell.Appearance.FLAG_INCORRECT: '#',
        Cell.Appearance.UNENCOUNTERED_BOMB: '*',
        Cell.Appearance.OPENED_BOMB: '!',
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8',
     }

    def __init__(self):
        """Creates difficulty and menus.

        Does not create a game (that does not happen until the user makes their
        first move, to prevent instant death.

        """
        self.difficulty = Difficulty()
        # self.game should be None before a game starts and during the time
        # after a game ends and before another one starts.
        self.game = None

        # --------------------
        # Menu attributes (listed in reverse order of when they are called)

        # Not initialized till self.game is initialized since it requires a
        # game to perform its actions.
        self.turn_menu = None

        self.first_turn_menu = ActionMenu(
            self.FIRST_TURN_MENU_DESCRIPTIONS,
            (self.open_first_cell,
             self.quit_and_end_program),
        )

        self.new_game_menu = ActionMenu(
            self.NEW_GAME_MENU_DESCRIPTIONS,
            [self.choose_level(level) for level in Difficulty.Level],
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
        """Start the TUI game by running its main menu.

        Returns
        -------
        None

        """
        self.main_menu.run_action_for_user_option()

    # -------------------------------------------------------------------------
    # New game menu functions

    def choose_level(self, level):
        """Makes a callable dependent on the level. Callable is responsible for
        setting difficulty to the given ``level`` and then starting the game.

        Parameters
        ----------
        level: Difficulty.Level
            Level to set the difficulty to.

        Returns
        -------
        callable

        """
        def difficulty_callable():
            """Set the games difficulty to ``level``

            Preconditions
            -------------
            - self.game is None before called.

            Postconditions
            --------------
            - The difficulty specs will be set per the user's choice.

            """
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

    # -------------------------------------------------------------------------
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
    # Board printing methods.

    def display_board_to_user(self):
        """Prints game statistics and either dummy or real board.

        Prints dummy board if it's the first turn (i.e. self.game not
        initialized since game is not initialized until after the user makes
        their first move due to bomb generation to prevent instant death).

        Returns
        -------
        None

        """
        self.print_turn()
        self.print_board()

    def print_turn(self):
        turns_taken = 0 if self.game is None else self.game.get_turn()
        print(f"\n(Legal) Turns taken: {turns_taken}")

    def print_board(self):
        if self.game is None:  # print dummy board
            rows, cols, _ = self.difficulty.get_diff_specs()
            unopened_char = self.APPEARANCES[Cell.Appearance.UNOPENED]
            board_strings = [[unopened_char for _ in range(cols)]
                             for _ in range(rows)]
        else:  # print real board
            board_strings = [[self.APPEARANCES[appearance] for appearance in row]
                             for row in self.game.get_all_appearances()]

        print(TablePrinter.makeTable(board_strings))

    # --------------------------------------------------------------------------
    # Turn menu methods

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
            self.game = None  # Remove the old game for display_board_to_user()
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
