class TerminalUI():
    """User interface for command line version of the game.

    """
    BASE = 10
    SEP = "+"
    LINE = "-"
    WALL = "|"

    def __init__(self, board):
        """Creates a new Terminal UI.

        Parameters
        ----------
        board: Board
            Minesweeper game board.

        """
        self.board = board
        self.HEIGHT = board.get_height()
        self.WIDTH = board.get_width()
        self.CELL_WIDTH = max(self.digit_count(self.HEIGHT) - 1,
                              self.digit_count(self.WIDTH) - 1) + 2
        self.UNIT_CEIL = self.CELL_WIDTH * self.LINE

    @staticmethod
    def digit_count(num):
        tmp = -num if num < 0 else num
        digit_count = 1
        tmp /= TerminalUI.BASE

        while tmp != 0:
            tmp //= TerminalUI.BASE
            digit_count += 1
        return digit_count

    def place_elt_in_cell(self, elt):
        return str(elt).center(self.CELL_WIDTH)

    def make_row(self, contents=None, seperator=None):
        if contents is None:
            contents = ["" for _ in range(self.WIDTH + 1)]

        if len(contents) < 1 + self.WIDTH:
            raise NotEnoughContents(1 + self.WIDTH, contents)
        if len(contents) > 1 + self.WIDTH:
            raise TooMuchContents(1 + self.WIDTH, contents)

        if seperator is None:
            seperator = self.WALL

        row = self.place_elt_in_cell(contents[0])  # usually row num col

        for elt in contents[1:]:
            row += f'{seperator}{self.place_elt_in_cell(elt)}'

        return f'{self.WALL}{row}{self.WALL}'

    def make_divider(self):
        return self.make_row([self.UNIT_CEIL for _ in range(1 + self.WIDTH)],
                             self.SEP)

    def make_col_num_row(self):
        return self.make_row([''] + [i for i in range(self.WIDTH)])

    def render_board(self):
        divider = self.make_divider()
        rendered = divider
        rendered += f"\n{self.make_col_num_row()}"
        rendered += f"\n{divider}"
        for i in range(self.HEIGHT):
            rendered += f"\n{self.make_row([i] + self.board.get_grid()[i])}"
            rendered += f"\n{divider}"
        return rendered


class TerminalUIError(Exception):
    pass


class NotEnoughContents(TerminalUIError):
    def __init__(self, required, contents):
        msg = f"(required, actual): ({required}, {len(contents)})"
        super().__init__(msg)


class TooMuchContents(TerminalUIError):
    def __init__(self, required, contents):
        msg = f"(required, actual): ({required}, {len(contents)})"
        super().__init__(msg)
