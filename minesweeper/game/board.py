from minesweeper.game.cell import Cell
from minesweeper.game.position_util import PositionUtil


class Board:
    DEFAULT_SIZE = 10

    def __init__(self, bombs):
        Board.validate_bombs(bombs)
        self.opened_count = 0
        self.bombs_opened_count = 0
        self.pos_util = PositionUtil(len(bombs), len(bombs[0]))
        self.grid = [[Cell(i, j, bomb=bomb) for j, bomb in enumerate(row)]
                     for i, row in enumerate(bombs)]

    @staticmethod
    def validate_bombs(bombs):
        if not all(len(bombs[0]) == len(row) for row in bombs):
            raise JaggedMinePositionsError(bombs)

    def get_shape(self):
        return (self.width, self.height)

    def get_grid(self):
        return self.grid

    def get_cell(self, row, col):
        return self.grid[row][col]

    def iterate(self, fcn):
        """Call a function on each of the cells in the grid.

        Parameters
        ----------
        fcn: function
            Must take a single parameter representing the cell.

        Returns
        -------
        None
        """
        for row in self.grid:
            for cell in row:
                fcn(cell)

    def reveal_mines(self, revealed):
        def reveal_mine(cell):
            if cell.is_bomb():
                cell.set_appearance(Cell.Appearance.UNENCOUNTERED_BOMB if revealed else
                                    Cell.Appearance.UNOPENED)

        self.iterate(reveal_mine)

    def __repr__(self):
        return '\n'.join(' '.join(repr(cell) for cell in row) for row in self.grid)

    # -----------------------------------------------------------------------------
    # Player move methods

    def open_cell(self, opened_row, opened_col):
        cell = self.grid[opened_row][opened_col]

        if cell.appearance != Cell.Appearance.UNOPENED:  # invalid move
            return False

        if cell.is_bomb():
            return self.open_bomb()

        self.opened_count += 1

        adj_cells = self.get_adjacent_cells(opened_row, opened_col)
        adj_bomb_count = Board.count_adjacent_bombs(adj_cells)
        cell.open_cell(adj_bomb_count)

        if adj_bomb_count == 0:
            for adj_cell in adj_cells:
                self.open_cell(self.get_cell(*adj_cell.get.pos()))

        return True  # valid move

    def open_bomb(self, cell):
        self.bombs_opened_count += 1
        cell.open_cell()
        return True

    def get_adjacent_cells(self, row, col):
        return [self.get_cell(*pos) for pos in self.pos_util.adj(row, col)]

    @staticmethod
    def count_adjacent_bombs(adjacent_cells):
        return sum(adj_cell.is_bomb() for adj_cell in adjacent_cells)


    def toggle_flag(self, row, col):
        """Toggle the flag of an unopened cell or a flagged cell.

        If the cell has any other appearance other than unopened or flag,
        returns false and does not alter appearance.

        Parameters
        ----------
        row: int
        col: int

        Returns
        -------
        bool
            Whether or not the toggle was valid.

        """
        cell = self.grid[row][col]
        return cell.toggle_flag()


class BoardError(Exception):
    def __init__(self, message):
        super().__init__(message)


class JaggedMinePositionsError(BoardError):
    def __init__(self, mine_positions):
        super().__init__('mine_positions is a jagged 2D list! Row lengths are:'
                         ' '.join(str(len(row)) for row in mine_positions))


if __name__ == '__main__':
    pass
