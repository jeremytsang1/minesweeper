from enum import Enum
from minesweeper.game.cell import Cell

class Move():
    """Class representing a player's move

    """
    class MoveType(Enum):
        OPEN = 1
        TOGGLE_FLAG = 2
        CHORD = 3

    CHORD_MSG = "Can only chord NUMBER cells."

    MSG = {
        MoveType.OPEN: {
            Cell.Appearance.FLAG: "Can't open a FLAGGED cell! Unflag it first!",
            Cell.Appearance.NUMBER: "Can't open a NUMBER cell!",
            Cell.Appearance.EMPTY: "Can't open an EMPTY cell!",
            Cell.Appearance.UNOPENED: None,
        },
        MoveType.TOGGLE_FLAG: {
            Cell.Appearance.FLAG: None,
            Cell.Appearance.NUMBER: "Can't toggle flag of a NUMBER cell!",
            Cell.Appearance.EMPTY: "Can't toggle flag of an EMPTY cell!",
            Cell.Appearance.UNOPENED: None,
        },
        MoveType.CHORD: {
            Cell.Appearance.FLAG: CHORD_MSG,
            Cell.Appearance.NUMBER: {
                # whether or not the number of flagged is equal to the number
                True: None,
                False: (
                    "Can only chord when the number of adjacent flags is "
                    "equal to the number."
                )
            },
            Cell.Appearance.EMPTY: CHORD_MSG,
            Cell.Appearance.UNOPENED: CHORD_MSG
        },
    }

    def __init__(self, valid, cell, move_type, adjFlagCount=None):
        self.valid = valid
        self.cell = cell
        self.move_type = move_type
        self.adjFlagCount = adjFlagCount

    def get_message(self):
        app = self.cell.get_appearance()
        msg = self.MSG[self.move_type][app]

        if (app == Cell.Appearance.NUMBER and self.move_type == self.MoveType.CHORD):
            assert type(self.adjFlagCount) == int
            assert type(self.cell.get_count) == int
            assert type(msg) == dict
            msg = msg[self.cell.get_count == self.adjFlagCount]

        return msg
