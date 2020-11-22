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

    def make_divider(self):
        result = self.UNIT_CEIL

        for _ in range(self.WIDTH):
            result += self.SEP + self.UNIT_CEIL

        return f'{self.WALL}{result}{self.WALL}'
