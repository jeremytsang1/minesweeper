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
    MIN_BOMB_COUNT = 1  # Needs to be positive.
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
        f"[{MIN_BOMB_COUNT} (inclusive) ... {{}} (exclusive)])"
    )

    START_GAME_MESSAGE = (
        "Starting {} game!"
        "\nheight: {}"
        "\n width: {}"
        "\n bombs: {}"
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

    ROW_PROMPT = "\nWhich row?"
    COL_PROMPT = "\nWhich col?"

    ILLEGAL_MOVE_MESSAGE = "\nIllegal move!"
    WON_MESSAGE = f"\nYOU WIN!{AsciiArt.HAPPY}"
    LOSS_MESSAGE = f"\nYOU DIED!{AsciiArt.DEAD}"

    GOODBYE = "\nGoodbye!"

    TURN_MESSAGE = "\n(Legal) Turns taken: {}"

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
            (self._open_first_cell,
             self._quit_and_end_program),
        )

        self.new_game_menu = ActionMenu(
            self.NEW_GAME_MENU_DESCRIPTIONS,
            [self._choose_level(level) for level in Difficulty.Level],
        )

        # Must be initialized after self.new_game_menu since it's action is
        # dependent on said attribute's existence.
        self.main_menu = ActionMenu(
            self.MAIN_MENU_DESCRIPTIONS,
            (self.new_game_menu.run_action_for_user_option,
             self._quit_and_end_program),
        )

    # -------------------------------------------------------------------------
    # Main menu methods

    def start(self):
        """Start the TUI game by running its main menu.

        Returns
        -------
        None

        """
        self.main_menu.run_action_for_user_option()

    # ----------------------------------------
    # New game menu methods

    def _choose_level(self, level):
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
                self.difficulty.set_specs(*self._read_custom_specs())

            print(self.START_GAME_MESSAGE.format(
                self.difficulty.get_current_level(),
                *self.difficulty.get_diff_specs()))
            self._display_board_to_user()
            self.first_turn_menu.run_action_for_user_option()

        return difficulty_callable

    @staticmethod
    def _read_custom_specs():
        """Prompt the player to enter in number of rows, columns, and bombs.

        Returns
        -------
        tuple of int
            Tuple of size three containing number of rows, columns, and bombs.

        """
        height = IO.read_int(TUI.HEIGHT_PROMPT, 1, TUI.MAX_INT)
        min_cols = 1 if height != 1 else 2  # prevent 1x1 grid
        width = IO.read_int(TUI.WIDTH_PROMPT, min_cols, TUI.MAX_INT)
        max_bomb_count = height * width
        bomb_count = IO.read_int(
            TUI.BOMB_PROMPT.format(max_bomb_count),
            min_val=TUI.MIN_BOMB_COUNT,
            max_val=max_bomb_count,
        )
        return height, width, bomb_count

    # ----------------------------------------
    # First turn menu methods

    def _open_first_cell(self):
        """Allow user to make their first move and create new game based on it.

        Returns
        -------
        None

        """
        pos = self._get_position_from_user()
        self.game = Game(*self.difficulty.get_diff_specs(), *pos)

        # Initialize a new turn_menu. Its actions are dependent on current
        # game.
        self.turn_menu = ActionMenu(
            self.TURN_MENU_DESCRIPTIONS,
            (*(self._take_turn(action) for action in self.game.get_actions()),
             self._quit_and_end_program),
        )
        self._process_move(self.game.open_cell(*pos))  # enact first turn

    # ----------------------------------------
    # Turn menu methods

    def _take_turn(self, player_action):
        """Make callable to simulate player taking their turn.

        Parameters
        ----------
        player_action: callable
            Callable to allow the player to perform a specific action during
            their turn.

        Returns
        -------
        callable
            Function that gets input and then decides if a move using that
            input is valid.

        """

        def perform_player_action():
            """Get user input perform move and go to check if the move is valid.

            """
            pos = self._get_position_from_user()
            move = player_action(*pos)   # Returns a move
            self._process_move(move)

        return perform_player_action

    def _process_move(self, move):
        """Check if a move is valid.

        Depending on the validity of the move either accept it as valid and
        continue normal game flow or warn the player why the move was invalid.

        Parameters
        ----------
        move: Move
            Move of the most recent turn.

        Returns
        -------
        None

        """
        assert type(move) == Move
        game_ended = False

        if move.is_valid():
            game_ended = self._is_game_over()
        else:
            print(self.ILLEGAL_MOVE_MESSAGE,
                  MoveMessage.MOVE_MESSAGE[move.get_reason_turn_is_invalid()])

        self._display_board_to_user()

        if game_ended:
            self._handle_end_game()
        else:
            self.turn_menu.run_action_for_user_option()

    def _is_game_over(self):
        """Predicate.

        Check end game conditions and decide whether to keep playing or stop.

        Returns
        -------
        bool
            Whether or not the game ended.

        """
        won, loss = self.game.check_end_game()
        return won or loss

    # -------------------------------------------------------------------------
    # Board printing methods.

    def _display_board_to_user(self):
        """Prints game statistics and either dummy or real board.

        Prints dummy board if it's the first turn (i.e. self.game not
        initialized since game is not initialized until after the user makes
        their first move due to bomb generation to prevent instant death).

        Returns
        -------
        None

        """
        turn_taken = 0 if self.game is None else self.game.get_turn()

        print(
            self.TURN_MESSAGE.format(turn_taken),
            self._make_board_output(),
            sep="\n"
        )

    def _make_board_output(self):
        """Create grid version of board with row and column numbers.

        Returns
        -------
        str
            Representation of the board of the current state of the game.

        """
        # Use dummy board if it is before first turn because game not
        # initialized till after player's first turn (in order to lay bombs in
        # a way to prevent instant death).
        if self.game is None:  # print dummy board
            rows, cols, _ = self.difficulty.get_diff_specs()
            unopened_char = self.APPEARANCES[Cell.Appearance.UNOPENED]
            board_strings = [[unopened_char for _ in range(cols)]
                             for _ in range(rows)]
        else:  # print real board
            board_strings = [[self.APPEARANCES[appearance] for appearance in row]
                             for row in self.game.get_all_appearances()]

        return TablePrinter.makeTable(board_strings)

    # -------------------------------------------------------------------------
    # End game and quitting methods

    def _handle_end_game(self):
        """Alert user they won/lost and allow them choice to start new game.

        Returns
        -------
        None

        """
        won, _ = self.game.check_end_game()
        self._show_end_game_results(won)
        self.game = None  # Remove the old game for display_board_to_user()
        self.start()

    def _show_end_game_results(self, won):
        """Print message depending on if user won or lost.

        Preconditions
        -------------
        User must have either won or lost the game.

        Parameters
        ----------
        won: bool
            Whether or not the user won the game.

        Returns
        -------
        None

        """
        print(TUI.WON_MESSAGE if won else TUI.LOSS_MESSAGE)

    @staticmethod
    def _quit_and_end_program():
        """Display a parting message to the user.

        Returns
        -------
        None

        """
        print(f'{TUI.GOODBYE}')

    # -------------------------------------------------------------------------
    # Input methods

    def _get_position_from_user(self):
        """Assumes a game is currently running.

        Gets position by first asking for row and then for column.

        Returns
        -------
        tuple of int
            Returns position that user entered.
        """
        row = IO.read_int(TUI.ROW_PROMPT, 0, self.difficulty.get_rows())
        col = IO.read_int(TUI.COL_PROMPT, 0, self.difficulty.get_cols())
        return row, col


if __name__ == '__main__':
    tui = TUI()
    tui.start()
