from minesweeper.game.board import Board
from minesweeper.game.bomb_dropper import BombDropper
from minesweeper.game.move import Move


class Game:
    MIN_WIDTH = 1
    MIN_HEIGHT = 1
    DEFAULT_SIZE = 10
    MIN_BOMB_COUNT = 1

    def __init__(self, height, width, bomb_count=1,
                 first_click_row=0, first_click_col=0):
        self.bomb_count = bomb_count

        if height < Game.MIN_HEIGHT or width < Game.MIN_WIDTH:
            raise GameNegativeDimsError(height, width)

        self.bomb_dropper = BombDropper(height, width, first_click_row,
                                        first_click_col, bomb_count)

        self.board = Board(self.bomb_dropper.drop_bombs())
        self.turn = 1  # Always start new game after user makes the first move.
        self.won = False
        self.loss = False
        # TODO: make the first move with the board

    # -----------------------------------------------------------------------------
    # PUBLIC # TODO rename since there is no privacy modifiers in python

    def open_cell(self, row, col):
        print("\nOpening!")
        # should return if move was valid or not
        # TODO increment self.turn if valid
        self.update_end_game()
        assert False, "Not yet implemented"

    def toggle_flag(self, row, col):
        print("Toggling flag!")
        valid = self.board.toggle_flag(row, col)
        move = Move(valid, self.board.get_cell(row, col), Move.MoveType.TOGGLE_FLAG)
        self.increment_turn(move)
        return move

    def chord_cell(self, row, col):
        print("\nChording!")
        # should return if move was valid or not
        # TODO increment self.turn if valid
        self.update_end_game()
        assert False, "Not yet implemented"

    def increment_turn(self, move):
        if move.is_valid():
            self.turn += 1

    def update_end_game(self):
        assert False, "Not yet implemented"

    def check_end_game(self):
        assert not (self.won and self.loss)
        return self.won, self.loss

    def reveal_board(self):
        assert False, "Not yet implemented"

    def get_turn(self):
        return self.turn

    def get_grid(self):
        return self.board.get_grid()

    # -----------------------------------------------------------------------------
    # PRIVATE # TODO rename since there is no privacy modifiers in python

    def check_victory(self):
        assert False, "Not yet implemented"

    def check_loss(self):
        assert False, "Not yet implemented"


class GameError(Exception):
    def __init__(self, message):
        super().__init__(message)


class GameNegativeDimsError(GameError):
    def __init__(self, height, width):
        super().__init__('Cannot create Game with negative dimensions '
                         f'({height}, {width}).')


class GameInvalidBombCount(GameError):
    def __init__(self, bomb_count):
        super().__init__('Cannot create Game with less than '
                         f'{Game.MIN_BOMB_COUNT} bombs.')
