from minesweeper.game.cell import Cell


class Board:
    def __init__(self, height, width):
        if height < 0 or width < 0:
            raise BoardNegativeDimsError(height, width)
        self.grid = [[Cell(i, j) for j in range(width)] for i in range(height)]
        self.height = height
        self.width = width

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_shape(self):
        return (self.width, self.height)

    def get_grid(self):
        return self.grid

    def __repr__(self):
        WIDTH = 3
        WALL = "|"
        SEP = "+"

    def build_row(self):
        pass


class BoardError(Exception):
    def __init__(self, message):
        super().__init__(message)


class BoardNegativeDimsError(BoardError):
    def __init__(self, height, width):
        super().__init__('Cannot create Board with negative dimensions '
                         f'({height}, {width}).')

if __name__ == '__main__':
    board = Board(5, 5)
