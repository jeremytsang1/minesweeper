from enum import Enum
from minesweeper.game.cell import Cell

class Move():
    """Class representing a player's move

    """
    class MoveType(Enum):
        OPEN = 1
        TOGGLE_FLAG = 2
        CHORD = 3

    class Invalid(Enum):
        CANT_OPEN_FLAGGED = 1
        CANT_OPEN_NUMBER = 2
        CANT_OPEN_EMPTY = 3
        CANT_TOGGLE_NUMBER = 4
        CANT_TOGGLE_EMPTY = 5
        CAN_ONLY_CHORD_NUMBER_CELLS = 6
        CANT_CHORD_WITH_INVALID_FLAG_ADJ = 7

    VALIDITY_RULES = {
        MoveType.OPEN: {
            Cell.Appearance.FLAG: Invalid.CANT_OPEN_FLAGGED,
            Cell.Appearance.NUMBER: Invalid.CANT_OPEN_NUMBER,
            Cell.Appearance.EMPTY: Invalid.CANT_OPEN_EMPTY,
            Cell.Appearance.UNOPENED: None,
        },
        MoveType.TOGGLE_FLAG: {
            Cell.Appearance.FLAG: None,
            Cell.Appearance.NUMBER: Invalid.CANT_TOGGLE_NUMBER,
            Cell.Appearance.EMPTY: Invalid.CANT_TOGGLE_EMPTY,
            Cell.Appearance.UNOPENED: None,
        },
        MoveType.CHORD: {
            Cell.Appearance.FLAG: Invalid.CAN_ONLY_CHORD_NUMBER_CELLS,
            # allow chording if flag count equals number of adjacent bombs
            Cell.Appearance.NUMBER: {
                True: None,
                False: Invalid.CANT_CHORD_WITH_INVALID_FLAG_ADJ,
            },
            Cell.Appearance.EMPTY: Invalid.CAN_ONLY_CHORD_NUMBER_CELLS,
            Cell.Appearance.UNOPENED: Invalid.CAN_ONLY_CHORD_NUMBER_CELLS,
        },
    }

    def __init__(self,
                 valid,
                 cell,
                 move_type,
                 affected_positions=None,
                 adjFlagCount=None):
        self.valid = valid
        self.cell = cell
        self.move_type = move_type
        self.affected_positions = (set() if affected_positions is None else
                                   affected_positions)
        self.adjFlagCount = adjFlagCount

    def get_reason_turn_is_invalid(self):
        appearance = self.cell.get_appearance()
        reason = self.VALIDITY_RULES[self.move_type][appearance]

        if (appearance == Cell.Appearance.NUMBER and self.move_type == self.MoveType.CHORD):
            assert type(self.adjFlagCount) == int
            assert type(self.cell.get_count()) == int
            assert type(reason) == dict
            reason = reason[self.cell.get_count() == self.adjFlagCount]

        return reason

    def get_appearance(self):
        return self.cell.get_appearance()

    def get_affected_positions(self):
        return self.affected_positions

    def is_valid(self):
        return self.valid
