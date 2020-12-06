import pygame


class GUICell(pygame.sprite.Sprite):
    """Graphical representation of a Minesweeper cell."""
    WIDTH = 20
    HEIGHT = 20

    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((x, y))
        self.surf.fill(255, 255, 255)
