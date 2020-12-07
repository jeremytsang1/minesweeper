from enum import Enum


class Cell:
    class Appearance(Enum):
        FLAG = 1
        NUMBER = 2
        EMPTY = 3
        UNOPENED = 4
        # ----------------------------------------
        FLAG_INCORRECT = 5
        UNENCOUNTERED_BOMB = 6
        OPENED_BOMB = 7

    MIN_COUNT = 0
    MAX_COUNT = 8
    ERROR_COMPONENT_TYPE = "component must be an int but is"
    ERROR_COMPONENT_VALUE = "component must be positive but is"
    ERROR_FLAG_TYPE = "flag state must be type bool but is"
    ERROR_COUNT_TYPE = "count must be an int"
    ERROR_COUNT_VALUE = ("count must be between Cell.MIN_COUNT,"
                         " Cell.MAX_COUNT")

    TEXT_APPEARANCE_RULES = {
        Appearance.FLAG: 'F',
        Appearance.EMPTY: ' ',
        Appearance.UNOPENED: '?',
        Appearance.FLAG_INCORRECT: '#',
        Appearance.UNENCOUNTERED_BOMB: '*',
        Appearance.OPENED_BOMB: '!',
    }

    def __init__(self, row, col, bomb=False):
        self.validate_components(row, col)

        self.row = row
        self.col = col
        self.bomb = bomb
        self.appearance = Cell.Appearance.UNOPENED
        self.count = None

    def validate_components(self, row, col):
        component_name = {row: "Row", col: "Col"}

        for component in (row, col):
            if type(component) != int:
                msg = (f'{component_name[component]} '
                       f'{Cell.ERROR_COMPONENT_TYPE} '
                       f'{component} (type {type(component)})')
                raise TypeError(msg)
            elif component < 0:
                msg = (f'{component_name[component]} '
                       f'{Cell.ERROR_COMPONENT_VALUE} '
                       f'{component}')
                raise ValueError(msg)
            else:
                pass  # Component is valid.

    # -------------------------------------------------------------------------
    # Getters

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def is_bomb(self):
        return self.bomb

    def get_appearance(self):
        return self.appearance

    def get_count(self):
        return self.count

    # ----------------------------------------

    def get_pos(self):
        return self.row, self.col

    # -------------------------------------------------------------------------
    # Methods for player actions.

    def toggle_flag(self):
        if self.appearance == Cell.Appearance.UNOPENED:
            self.appearance = Cell.Appearance.FLAG
        elif self.appearance == Cell.Appearance.FLAG:
            self.appearance = Cell.Appearance.UNOPENED
        else:
            return False  # invalid move
        return True  # valid move

    def set_flag_if_bomb(self):
        if self.bomb:
            self.appearance = Cell.Appearance.FLAG

    def set_count(self, count):
        """Opens a cell and sets it number.

        Parameters
        ----------
        count: int
            Integer between Cell.MIN_COUNT and Cell.MAX_COUNT (inclusive for
            both).

        Returns
        -------
        None
        """
        self.validate_count(count)
        self.count = count
        if self.count == 0:
            self.appearance = Cell.Appearance.EMPTY
        else:
            self.appearance = Cell.Appearance.NUMBER

    def validate_count(self, count):
        if self.bomb:
            raise IllegalSetCountBomb(self.row, self.col)
        elif self.count is not None:
            raise AttemptToResetCountError(self.row, self.col)
        elif type(count) != int:
            raise TypeError(Cell.ERROR_COUNT_TYPE)
        elif count not in range(Cell.MIN_COUNT, Cell.MAX_COUNT + 1):
            raise ValueError(Cell.ERROR_COUNT_VALUE)
        else:
            pass  # Count is valid.

    def open_cell(self, adj_bomb_count=None):
        """Responsible for updating the appearance of the cell after opening"""
        if self.is_bomb():
            self.appearance = Cell.Appearance.OPENED_BOMB
        elif type(adj_bomb_count) == int:
            self.set_count(adj_bomb_count)
        else:
            raise OpenInvalidArgument(self.row, self.col)

    # -------------------------------------------------------------------------
    # Display methods.

    def set_appearance(self, appearance):
        self.appearance = appearance

    def reveal_unopened_bomb(self):
        if self.appearance == Cell.Appearance.UNOPENED and self.bomb:
            self.appearance = Cell.Appearance.UNENCOUNTERED_BOMB

    def text_appearance(self):
        if self.appearance == Cell.Appearance.NUMBER:
            return str(self.count)
        else:
            return Cell.TEXT_APPEARANCE_RULES[self.appearance]

    def __repr__(self):
        return self.text_appearance()

    def __str__(self):
        return self.text_appearance()


class CellError(Exception):
    """Base exception class for objects of type Cell."""
    def __init__(self, message):
        super().__init__(message)


class IllegalFlagToggle(CellError):
    """When a user clicks a flag attempting to open it."""
    def __init__(self, row, col):
        super().__init__(
            f"Toggling a cell at ({row}, {col}) "
            "which isn't unopened or flagged."
        )


class IllegalSetCountBomb(CellError):
    def __init__(self, row, col):
        super().__init__(
            f"Tried to set count of cell at ({row}, {col}) but it's a bomb."
        )


class AttemptToResetCountError(CellError):
    def __init__(self, row, col):
        super().__init__(
            f"Tried to set count of cell at ({row}, {col}) but it already has "
            "been set."
        )


class OpenInvalidArgument(CellError):
    def __init__(self, row, col):
        super().__init__(
            f"Opening cell at ({row}, {col}) failed. Not a bomb but "
            "adjacent bomb count is not given as an int."
        )
