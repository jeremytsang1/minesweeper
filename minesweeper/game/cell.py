from enum import Enum


class Cell:
    class Appearance(Enum):
        FLAG = 1
        NUMBER = 2
        EMPTY = 3
        UNOPENED = 4
        FLAG_INCORRECT = 5
        UNENCOUNTERED_BOMB = 6
        DEATH_LOCATION = 7

    MIN_COUNT = 0
    MAX_COUNT = 8
    ERROR_COMPONENT_TYPE = "component must be an int but is"
    ERROR_COMPONENT_VALUE = "component must be positive but is"
    ERROR_COUNT_TYPE = "adj_bomb_count must be an int"
    ERROR_COUNT_VALUE = ("adj_bomb_count must be between Cell.MIN_COUNT,"
                         " Cell.MAX_COUNT")

    TEXT_APPEARANCE_RULES = {
        Appearance.FLAG: 'F',
        Appearance.EMPTY: ' ',
        Appearance.UNOPENED: '?',
        Appearance.FLAG_INCORRECT: '#',
        Appearance.UNENCOUNTERED_BOMB: '*',
        Appearance.DEATH_LOCATION: '!',
    }

    def __init__(self, row, col, bomb=False):
        self.validate_component(row, col)

        self.row = row
        self.col = col
        self.bomb = bomb
        self.opened = False
        self.appearance = Cell.Appearance.UNOPENED
        self.adj_bomb_count = None

    def validate_component(self, row, col):
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
                pass

    def validate_count(self, count):
        if type(count) != int:
            raise TypeError(Cell.ERROR_COUNT_TYPE)
        elif count not in range(Cell.MIN_COUNT, Cell.MAX_COUNT + 1):
            raise ValueError(Cell.ERROR_COUNT_VALUE)
        else:
            pass

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def set_adj_bomb_count(self, count):
        self.validate_count(count)
        self.adj_bomb_count = count

    def get_adj_bomb_count(self):
        return self.adj_bomb_count

    def set_opened(self):
        self.opened = True

    def get_opened(self):
        return self.opened

    def is_bomb(self):
        return self.bomb

    def get_appearance(self):
        return self.appearance

    def set_appearance(self, appearance):
        self.appearance = appearance

    def text_appearance(self):
        if self.appearance == Cell.Appearance.NUMBER:
            self.validate_count(self.adj_bomb_count)  # make sure not None
            return str(self.adj_bomb_count)
        else:
            return Cell.TEXT_APPEARANCE_RULES[self.appearance]

    def __repr__(self):
        return self.text_appearance()

    def __str__(self):
        return self.text_appearance()
