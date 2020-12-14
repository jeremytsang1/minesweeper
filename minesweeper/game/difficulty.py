from enum import Enum


class Difficulty():
    """Determines shape of board and number of bombs."""

    class Level(Enum):
        """Preset difficulties."""
        EASY = 1
        MEDIUM = 2
        HARD = 3
        CUSTOM = 4

    PRESETS = {
        Level.EASY: (10, 10, 10),
        Level.MEDIUM: (16, 16, 40),
        Level.HARD: (16, 30, 99),
    }

    def __init__(self):
        self.rows = None
        self.cols = None
        self.bomb_count = None
        self.current_level = None

        # Initialize at easy difficulty
        self.set_preset_level(Difficulty.Level.EASY)

    def __repr__(self):
        return (
            '(rows, cols, bomb_count): '
            f'{self.rows}, {self.cols}, {self.bomb_count}'
        )

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def get_shape(self):
        return (self.rows, self.cols)

    def get_bomb_count(self):
        return self.bomb_count

    def get_diff_specs(self):
        return self.rows, self.cols, self.bomb_count

    def get_current_level(self):
        return self.current_level

    def set_difficulty(self, level):
        self.current_level = level

        # TODO: find way to set rows, cols, bombs here

        if level == Difficulty.Level.CUSTOM:
            return False
        elif level in Difficulty.PRESETS:
            self.set_preset_level(level)
            return True
        else:
            raise ValueError("`level` is not a valid Difficulty.Level")

    def set_preset_level(self, level):
        self.set_specs(*Difficulty.PRESETS[level])

    def set_specs(self, rows, cols, bomb_count):
        self.rows = rows
        self.cols = cols
        self.bomb_count = bomb_count
