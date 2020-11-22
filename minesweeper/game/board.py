from minesweeper.game.cell import Cell


class Board:
    MIN_WIDTH = 1
    MIN_HEIGHT = 1

    def __init__(self, height, width):
        if height < Board.MIN_HEIGHT or width < Board.MIN_WIDTH:
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
        return '\n'.join(' '.join(repr(cell) for cell in row) for row in self.grid)

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
