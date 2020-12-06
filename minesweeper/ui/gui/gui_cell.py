import pygame
from pygame.locals import (
    RLEACCEL
)
from minesweeper.game.cell import Cell
import os


class GUICell(pygame.sprite.Sprite):
    """Graphical representation of a Minesweeper cell."""
    WIDTH = 30
    HEIGHT = 30
    BORDER_WIDTH = 2
    CELL_SPACING = 0
    DIR_IMG = os.path.join('minesweeper', 'ui', 'gui', 'assets', 'img')
    DIR_BOMBS = os.path.join(DIR_IMG, 'bombs')
    DIR_NUMBERS = os.path.join(DIR_IMG, 'numbers')
    DIR_FLAGS = os.path.join(DIR_IMG, 'flags')
    DIR_SQUARES = os.path.join(DIR_IMG, 'squares')

    # Can't use comprehensions in class level variables:
    # https://stackoverflow.com/a/28130950
    IMAGES = {
        1: {'filename': os.path.join(DIR_NUMBERS, '1.png'), 'fill': '#ffffff'},
        2: {'filename': os.path.join(DIR_NUMBERS, '2.png'), 'fill': '#ffffff'},
        3: {'filename': os.path.join(DIR_NUMBERS, '3.png'), 'fill': '#ffffff'},
        4: {'filename': os.path.join(DIR_NUMBERS, '4.png'), 'fill': '#ffffff'},
        5: {'filename': os.path.join(DIR_NUMBERS, '5.png'), 'fill': '#ffffff'},
        6: {'filename': os.path.join(DIR_NUMBERS, '6.png'), 'fill': '#ffffff'},
        7: {'filename': os.path.join(DIR_NUMBERS, '7.png'), 'fill': '#ffffff'},
        8: {'filename': os.path.join(DIR_NUMBERS, '8.png'), 'fill': '#ffffff'},
        # 'square_black': os.path.join(DIR_SQUARES, 'square_black.png'),
        Cell.Appearance.FLAG: {'filename': os.path.join(DIR_FLAGS, 'flag.png'), 'fill': '#FFFFFF'},
        Cell.Appearance.UNOPENED: {'filename': os.path.join(DIR_SQUARES, 'square_blue.png'), 'fill': '#000000'},
        Cell.Appearance.EMPTY: {'filename': os.path.join(DIR_SQUARES, 'square_empty.png'), 'fill': '#000000'},
        Cell.Appearance.UNENCOUNTERED_BOMB: {'filename': os.path.join(DIR_BOMBS, 'bomb_black.png'), 'fill': '#000000'},
        Cell.Appearance.OPENED_BOMB: {'filename': os.path.join(DIR_BOMBS, 'bomb_red.png'), 'fill': '#000000'},
    }

    def __init__(self, x, y, row, col):
        super().__init__()
        self.x = x
        self.y = y
        self.row_col_pos = (row, col)
        self.pos = (x, y)
        self.appearance = None  # start off with no appearance until loading
        self.load_image(Cell.Appearance.UNOPENED)

    def get_row_col_pos(self):
        return self.row_col_pos

    def position_cell(self):
        self.rect.move_ip(*self.pos)

    def load_image(self, appearance):
        # Don't bother updating if appearance hasn't changed.
        if self.appearance == appearance:
            return

        filename = self.IMAGES[appearance]['filename']
        fill = self.IMAGES[appearance]['fill']
        self.surf = pygame.image.load(filename).convert()
        self.surf.set_colorkey(fill, RLEACCEL)

        self.surf = self.shrink_down(self.surf)
        self.image = self.surf

        self.rect = self.surf.get_rect()
        self.position_cell()

    def draw(self, screen):
        # Draw rectangle around the cell.
        pygame.draw.rect(screen, "#000000", self.rect, 2)

    def shrink_down(self, surf):
        return pygame.transform.scale(
            surf,
            (self.WIDTH - self.CELL_SPACING * self.BORDER_WIDTH,
             self.HEIGHT - self.CELL_SPACING * self.BORDER_WIDTH),
        )

    def is_mouse_up(self, mouse):
        if self.rect.collidepoint(mouse):
            return True
        return False
