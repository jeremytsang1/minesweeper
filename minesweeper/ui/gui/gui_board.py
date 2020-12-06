import pygame
from minesweeper.ui.gui.gui_cell import GUICell


class GUIBoard():
    """Graphical representation of the Minesweeper board."""
    def __init__(self, rows, cols, offset_x=0, offset_y=0,):
        self.rows = rows
        self.cols = cols
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.gui_cells = pygame.sprite.Group()

    @staticmethod
    def compute_dimensions(rows, cols):
        width = GUICell.WIDTH * cols
        height = GUICell.HEIGHT * rows
        return [width, height]

    def kill_gui_board(self):
        for gui_cell in self.gui_cells:
            gui_cell.kill()
