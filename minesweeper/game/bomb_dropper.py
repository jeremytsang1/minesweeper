import random
from minesweeper.game.position_util import PositionUtil

class BombDropper():
    """

    """
    DEFAULT_SIZE = 10
    DEFAULT_CLICK_ROW = 0
    DEFAULT_CLICK_COL = 0
    DEFAULT_BOMB_COUNT = 1

    def __init__(self,
                 height=DEFAULT_SIZE,
                 width=DEFAULT_SIZE,
                 initial_click_row=DEFAULT_CLICK_ROW,
                 initial_click_col=DEFAULT_CLICK_COL,
                 bomb_count=DEFAULT_BOMB_COUNT):
        BombDropper.validate_input(height, width, initial_click_row,
                                   initial_click_col, bomb_count)
        self.height = height
        self.width = width
        self.pos_util = PositionUtil(self.height, self.width)
        self.bomb_count = bomb_count

    # -------------------------------------------------------------------------
    # Validation methods

    @staticmethod
    def validate_input(height, width, row, col, bomb_count):
        BombDropper.validate_components(height, width)
        BombDropper.validate_bomb_count(height, width, bomb_count)
        BombDropper.validate_initial_click(height, width, row, col)

    @staticmethod
    def validate_components(height, width):
        if height <= 0:
            raise InvalidComponent(height, "height")
        if width <= 0:
            raise InvalidComponent(width, "width")

    @staticmethod
    def validate_bomb_count(height, width, bomb_count):
        if bomb_count <= 0 or height * width <= bomb_count:
            raise InvalidBombCount(height, width, bomb_count)

    @staticmethod
    def validate_initial_click(height, width, row, col):
        if row not in range(height) or col not in range(width):
            raise InvalidInitialClick(height, width, row, col)

    # -------------------------------------------------------------------------
    # getters

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    # -------------------------------------------------------------------------
    # Bomb laying

    def initialize_empty_bomb_field(self):
        return [[False for _ in range(self.width)] for _ in range(self.height)]

    def drop_bombs(self):
        bombs = self.initialize_empty_bomb_field()
        first_position = (self.first_click_row, self.first_click_col)
        positions = self.pos_util.make_valid_positions()
        positions.remove(first_position)  # Avoid instant death on first turn.
        positions = list(positions)  # Allow for shuffling
        random.shuffle(positions)

        assert self.bomb_count <= len(positions)

        for row, col in positions[:self.bomb_count]:
            bombs[row][col] = True

        return bombs


class BombDropperError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidComponent(BombDropperError):
    def __init__(self, component, name):
        super().__init__(
            f'BombDropper\'s {name} is non-positive and has value {component}.'
        )


class InvalidBombCount(BombDropperError):
    def __init__(self, height, width, bomb_count):
        super().__init__(
            f'Invalid number of bombs ({bomb_count}) for {height} x {width}'
            + ' grid'
        )


class InvalidInitialClick(BombDropperError):
    def __init__(self, height, width, row, col):
        super().__init__(
            f'Initial click ({row}, {col})is outside {height} x {width} grid'
        )
