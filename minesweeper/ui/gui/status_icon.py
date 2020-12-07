import pygame
from pygame.locals import (
    RLEACCEL
)
import os
from enum import Enum


class StatusIcon(pygame.sprite.Sprite):
    WIDTH = 100
    HEIGHT = 100

    class Status(Enum):
        ALIVE = 1
        MOUSE_DOWN = 2
        LOSS = 3
        WIN = 4

    DIR_IMG = os.path.join('assets', 'img')
    DIR_EMOTICONS = os.path.join(DIR_IMG, 'emoticons')
    FILENAMES = {
        Status.ALIVE: os.path.join(DIR_EMOTICONS, "01-alive.png"),
        Status.MOUSE_DOWN: os.path.join(DIR_EMOTICONS, "02-mouse-down.png"),
        Status.LOSS: os.path.join(DIR_EMOTICONS, "03-dead.png"),
        Status.WIN: os.path.join(DIR_EMOTICONS, "04-win.png"),
    }
    FILL = "#FFFFFF"

    def __init__(self, x, y, width=None, height=None):
        super().__init__()
        self.width = self.WIDTH if width is None else width
        self.height = self.HEIGHT if height is None else height
        self.spatial_pos = (x, y)
        self.status = None
        self.load_image(self.Status.ALIVE)

    def load_image(self, status):
        # Don't bother updating if status hasn't changed.
        if self.status == status:
            return

        filename = self.FILENAMES[status]
        self.surf = pygame.image.load(filename).convert()
        self.surf.set_colorkey(self.FILL, RLEACCEL)
        self.surf = self.shrink_down(self.surf)
        self.image = self.surf

        self.rect = self.surf.get_rect()
        self.position_cell()

    def position_cell(self):
        self.rect.move_ip(*self.spatial_pos)

    def shrink_down(self, surf):
        return pygame.transform.scale(surf, (self.width, self.height))
