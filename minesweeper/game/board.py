from minesweeper.game.cell import Cell


class Board:
    DEFAULT_SIZE = 10

    def __init__(self, bombs):
        self.height = len(bombs)
        self.width = len(bombs[0])

        if not all(len(bombs[0]) == len(row) for row in bombs):
            raise JaggedMinePositionsError(bombs)

        self.grid = [[Cell(i, j, bomb=bomb) for j, bomb in enumerate(row)]
                     for i, row in enumerate(bombs)]
        assert False, "NOT YET IMPLEMENTED: Make sure to open the first cell"

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

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
