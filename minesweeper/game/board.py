from minesweeper.game.cell import Cell
from minesweeper.game.position_util import PositionUtil


class Board:
    DEFAULT_SIZE = 10

    def __init__(self, bombs):
        Board.validate_bombs(bombs)
        self.opened_cell_count = 0
        self.opened_bomb_count = 0
        pos_util = PositionUtil(len(bombs), len(bombs[0]))
        self.adj = pos_util.adj
        self.grid = [[Cell(i, j, bomb=bomb) for j, bomb in enumerate(row)]
                     for i, row in enumerate(bombs)]

    @staticmethod
    def validate_bombs(bombs):
        if not all(len(bombs[0]) == len(row) for row in bombs):
            raise JaggedMinePositionsError(bombs)

    def get_opened_cell_count(self):
        return self.opened_cell_count

    def get_opened_bomb_count(self):
        return self.opened_bomb_count

    def get_shape(self):
        return len(self.grid), len(self.grid[0])

    def get_grid(self):
        return self.grid

    def get_cell(self, row, col):
        return self.grid[row][col]

    def get_appearance(self):
        appearances = [[None for _ in row] for row in self.grid]

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                appearance = cell.get_appearance()
                if appearance is Cell.Appearance.NUMBER:
                    appearance = cell.get_count()

                appearances[i][j] = appearance

        return appearances

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
        def open_bomb(cell):
            self.opened_bomb_count += 1
            cell.open_cell()
            return True  # valid move

        def open_non_bomb_cell(opened_cell):
            self.opened_cell_count += 1
            adj_cells = self.get_adjacent_cells(opened_cell)
            adj_bomb_count = Board.count_adjacent_bombs(adj_cells)
            opened_cell.open_cell(adj_bomb_count)
            return adj_cells, adj_bomb_count

        opened_cell = self.grid[opened_row][opened_col]

        if opened_cell.appearance != Cell.Appearance.UNOPENED:  # invalid move
            return False

        if opened_cell.is_bomb():
            return open_bomb(opened_cell)

        adj_cells, adj_bomb_count = open_non_bomb_cell(opened_cell)

        if adj_bomb_count == 0:
            for adj_cell in adj_cells:
                self.open_cell(*adj_cell.get_pos())

        return True  # valid move

    def get_adjacent_cells(self, opened_cell):
        return [self.get_cell(*pos) for pos in self.adj(*opened_cell.get_pos())]

    @staticmethod
    def count_adjacent_bombs(cells):
        """Count the number of bombs in a group of cells.

        Parameters
        ----------
        cells: list of Cell
            Cells to count from.

        Returns
        -------
        int
        """
        return sum(cell.is_bomb() for cell in cells)

    @staticmethod
    def count_appearance(cells, appearance=Cell.Appearance.FLAG):
        """Count the number of occurences of a given Cell appearance.

        Parameters
        ----------
        cells: list of Cell
            Cells to count from.
        appearance: Cell.Appearance
            Appearance to count.

        Returns
        -------
        int
        """
        return sum(cell.get_appearance() == appearance for cell in cells)

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

    def chord_cell(self, row, col):
        cell = self.get_cell(row, col)
        adj_cells = self.get_adjacent_cells(cell)
        flag_count = Board.count_appearance(adj_cells)

        def is_valid_cell_to_chord():
            if cell.get_appearance() != Cell.Appearance.NUMBER:
                return False
            elif flag_count != cell.get_count():
                return False
            else:
                return True

        if not is_valid_cell_to_chord():
            return False, flag_count

        for adj_cell in adj_cells:
            if adj_cell.get_appearance() != Cell.Appearance.FLAG:
                self.open_cell(*adj_cell.get_pos())

        return True, flag_count

    def reveal_board(self):
        self.iterate(lambda cell: cell.reveal_unopened_bomb())


class BoardError(Exception):
    def __init__(self, message):
        super().__init__(message)


class JaggedMinePositionsError(BoardError):
    def __init__(self, mine_positions):
        super().__init__('mine_positions is a jagged 2D list! Row lengths are:'
                         ' '.join(str(len(row)) for row in mine_positions))


if __name__ == '__main__':
    pass
