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
    FILENAMES = {
        1: os.path.join(DIR_NUMBERS, '1.png'),
        2: os.path.join(DIR_NUMBERS, '2.png'),
        3: os.path.join(DIR_NUMBERS, '3.png'),
        4: os.path.join(DIR_NUMBERS, '4.png'),
        5: os.path.join(DIR_NUMBERS, '5.png'),
        6: os.path.join(DIR_NUMBERS, '6.png'),
        7: os.path.join(DIR_NUMBERS, '7.png'),
        8: os.path.join(DIR_NUMBERS, '8.png'),
        # 'square_black': os.path.join(DIR_SQUARES, 'square_black.png'),
        Cell.Appearance.FLAG: os.path.join(DIR_FLAGS, 'flag.png'),
        Cell.Appearance.UNOPENED: os.path.join(DIR_SQUARES, 'square_blue.png'),
        Cell.Appearance.EMPTY: os.path.join(DIR_SQUARES, 'square_empty.png'),
        Cell.Appearance.UNENCOUNTERED_BOMB: os.path.join(DIR_BOMBS, 'bomb_black.png'),
        Cell.Appearance.OPENED_BOMB: os.path.join(DIR_BOMBS, 'bomb_red.png'),
    }

    def __init__(self, x, y):
        super().__init__()
        self.load_image(Cell.Appearance.UNOPENED)

    def load_image(self, appearance):
        filename = self.FILENAMES[appearance]
        self.surf = pygame.image.load(filename).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        self.rect = self.surf.get_rect()
