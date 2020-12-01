from minesweeper.game.board import Board
from minesweeper.game.bomb_dropper import BombDropper


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
        self.turn = 0
        # TODO: make the first move with the board

    # -----------------------------------------------------------------------------
    # PUBLIC # TODO rename since there is no privacy modifiers in python

    def open_cell(self, row, col):
        print("\nOpening!")
        # should return if move was valid or not
        # TODO increment self.turn if valid
        assert False, "Not yet implemented"

    def toggle_flag(self, row, col):
        print("Toggling flag!")
        # should return if move was valid or not
        # TODO increment self.turn if valid
        assert False, "Not yet implemented"

    def chord_cell(self, row, col):
        print("\nChording!")
        # should return if move was valid or not
        # TODO increment self.turn if valid
        assert False, "Not yet implemented"

    def check_end_game(self):
        won = self.check_victory()
        loss = self.check_loss()
        assert not (won and loss)
        return won, loss

    def reveal_board(self):
        assert False, "Not yet implemented"

    def get_turn(self):
        return self.turn

    def get_grid(self):
        return self.board.get_grid()

    # -----------------------------------------------------------------------------
    # PRIVATE # TODO rename since there is no privacy modifiers in python

    def validate_init_input(self):
        self.validate_shape()
        self.validate_bomb_count()
        self.validate_first_move()

    def validate_shape(self):
        # TODO
        assert False, "Not yet implemented"

    def validate_bomb_count(self):
        # TODO
        assert False, "Not yet implemented"

    def validate_first_move(self):
        # TODO
        assert False, "Not yet implemented"

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
