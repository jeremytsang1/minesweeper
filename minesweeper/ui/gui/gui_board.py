import pygame
from minesweeper.ui.gui.gui_cell import GUICell


class GUIBoard():
    """Graphical representation of the Minesweeper board."""
    def __init__(self, rows, cols, offset_x=0, offset_y=0,):
        print(f'(rows, cols): {(rows, cols)}')
        self.rows = rows
        self.cols = cols
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.gui_cells_2D = []
        self.sprites = pygame.sprite.Group()
        self.spawn_cells()

    def get_gui_cells_2D(self):
        return self.gui_cells_2D

    def get_sprites(self):
        return self.sprites

    @staticmethod
    def compute_dimensions(rows, cols):
        width = GUICell.WIDTH * cols
        height = GUICell.HEIGHT * rows
        return [width, height]

    def kill_gui_board(self):
        for gui_cell in self.sprites:
            gui_cell.kill()

    def spawn_cells(self):
        """Create sprite to graphically represent each cell.

        Stores them in both a sprite Group as well as a standard 2D list. Uses
        the latter for convenient coordination with the business logic board.

        Returns
        -------
        None
            return description

        """
        for row in range(self.rows):
            self.gui_cells_2D.append([])
            for col in range(self.cols):
                gui_cell = GUICell(row, col)
                self.gui_cells_2D[row].append(gui_cell)
                self.sprites.add(gui_cell)
