class CommandLineGrid():
    """Board class for printing on command line."""
    BASE = 10
    SEP = "+"
    LINE = "-"
    WALL = "|"

    def __init__(self, height, width, cell_width=None):
        """Creates a new Commandline Grid.

        Parameters
        ----------
        board: Board
            Minesweeper game board.

        """
        self.HEIGHT = height
        self.WIDTH = width

        if cell_width is None:
            self.CELL_WIDTH = self.mininum_permissible_cell_width()
        else:
            self.CELL_WIDTH = min(cell_width,
                                  self.mininum_permissible_cell_width())

        self.UNIT_CEIL = self.CELL_WIDTH * self.LINE

    @staticmethod
    def digit_count(num):
        tmp = -num if num < 0 else num
        digit_count = 1
        tmp /= CommandLineGrid.BASE

        while tmp != 0:
            tmp //= CommandLineGrid.BASE
            digit_count += 1
        return digit_count

    def mininum_permissible_cell_width(self):
        return max(self.digit_count(self.HEIGHT) - 1,
                   self.digit_count(self.WIDTH) - 1) + 2

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

    @staticmethod
    def get_shape(itr_2d, row_num):
        return len(itr_2d), len(itr_2d[row_num])

    def validate_shape(self, itr_2d):
        if len(itr_2d) != self.HEIGHT:
            raise Iterable2DShapeIncompatible(
                self.WIDTH, self.HEIGHT, *self.get_shape(itr_2d, 0)
            )
        for i, row in enumerate(itr_2d):
            if len(row) != self.WIDTH:
                raise Iterable2DShapeIncompatible(
                    self.WIDTH, self.HEIGHT, *self.get_shape(itr_2d, i)
                )

    def make_table_from_itr_2d(self, itr_2d):
        self.validate_shape(itr_2d)

        divider = self.make_divider()
        rendered = divider
        rendered += f"\n{self.make_col_num_row()}"
        rendered += f"\n{divider}"

        for row_num in range(len(itr_2d)):
            rendered += (f"\n{self.make_row([row_num] + itr_2d[row_num])}"
                         f"\n{divider}")
        return rendered


class CommandLineGridError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NotEnoughContents(CommandLineGridError):
    def __init__(self, required, contents):
        msg = f"(required, actual): ({required}, {len(contents)})"
        super().__init__(msg)


class TooMuchContents(CommandLineGridError):
    def __init__(self, required, contents):
        msg = f"(required, actual): ({required}, {len(contents)})"
        super().__init__(msg)


class Iterable2DShapeIncompatible(CommandLineGridError):
    """Error for when the iterable trying to print doesn't have same size as the
    instance

    """
    def __init__(self, exp_width, exp_height, act_height, act_width):
        msg = (f"Expected shape: ({exp_height}, {exp_width})\n"
               f"Passed   shape: ({act_height}, {act_width})")
        super().__init__(msg)
