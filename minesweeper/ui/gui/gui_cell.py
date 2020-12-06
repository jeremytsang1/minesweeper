import pygame
from pygame.locals import (
    RLEACCEL
)
from minesweeper.game.cell import Cell
import os


class GUICell(pygame.sprite.Sprite):
    """Graphical representation of a Minesweeper cell."""
    WIDTH = 20
    HEIGHT = 20
    DIR_IMG = os.path.join('minesweeper', 'ui', 'gui', 'assets', 'img')
    DIR_BOMBS = os.path.join(DIR_IMG, 'bombs')
    DIR_NUMBERS = os.path.join(DIR_IMG, 'numbers')
    DIR_FLAGS = os.path.join(DIR_IMG, 'flags')
    DIR_SQUARES = os.path.join(DIR_IMG, 'squares')

    # Can't use comprehensions in class level variables:
    # https://stackoverflow.com/a/28130950
    IMAGES = {
        1: {'filename': os.path.join(DIR_NUMBERS, '1.png'), 'fill': '#000000'},
        2: {'filename': os.path.join(DIR_NUMBERS, '2.png'), 'fill': '#000000'},
        3: {'filename': os.path.join(DIR_NUMBERS, '3.png'), 'fill': '#000000'},
        4: {'filename': os.path.join(DIR_NUMBERS, '4.png'), 'fill': '#000000'},
        5: {'filename': os.path.join(DIR_NUMBERS, '5.png'), 'fill': '#000000'},
        6: {'filename': os.path.join(DIR_NUMBERS, '6.png'), 'fill': '#000000'},
        7: {'filename': os.path.join(DIR_NUMBERS, '7.png'), 'fill': '#000000'},
        8: {'filename': os.path.join(DIR_NUMBERS, '8.png'), 'fill': '#000000'},
        # 'square_black': os.path.join(DIR_SQUARES, 'square_black.png'),
        Cell.Appearance.FLAG: {'filename': os.path.join(DIR_FLAGS, 'flag.png'), 'fill': '#FFFFFF'},
        Cell.Appearance.UNOPENED: {'filename': os.path.join(DIR_SQUARES, 'square_blue.png'), 'fill': '#000000'},
        Cell.Appearance.EMPTY: {'filename': os.path.join(DIR_SQUARES, 'square_empty.png'), 'fill': '#000000'},
        Cell.Appearance.UNENCOUNTERED_BOMB: {'filename': os.path.join(DIR_BOMBS, 'bomb_black.png'), 'fill': '#000000'},
        Cell.Appearance.OPENED_BOMB: {'filename': os.path.join(DIR_BOMBS, 'bomb_red.png'), 'fill': '#000000'},
    }

    def __init__(self, x, y):
        super().__init__()
        self.load_image(Cell.Appearance.UNOPENED)

    def load_image(self, appearance):
        filename = self.IMAGES[appearance]['filename']
        fill = self.IMAGES[appearance]['fill']
        self.surf = pygame.image.load(filename).convert()
        self.surf.set_colorkey(fill, RLEACCEL)
        self.rect = self.surf.get_rect()
