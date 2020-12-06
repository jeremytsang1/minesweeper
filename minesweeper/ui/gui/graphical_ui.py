import pygame
from minesweeper.ui.gui.main_menu import MainMenu
from minesweeper.ui.gui.difficulty import Difficulty
from minesweeper.ui.gui.gui_board import GUIBoard
from minesweeper.game.game import Game


class GUI():
    def __init__(self):
        pygame.init()
        self.difficulty = Difficulty()
        self.game = None
        self.gui_board = None
        self.screen = pygame.display.set_mode((MainMenu.WIDTH,
                                               MainMenu.HEIGHT))
        self.main_menu = MainMenu(self.set_difficulty, self.run_game)

    def set_difficulty(self, description, level):
        self.difficulty.set_difficulty(level)

    def run_main_menu(self):
        self.screen = pygame.display.set_mode((MainMenu.WIDTH,
                                               MainMenu.HEIGHT))
        self.main_menu.show_menu(self.screen)

    def run_game(self):
        self.game = None
        dimensions = GUIBoard.compute_dimensions(*self.difficulty.get_shape())
        self.screen = pygame.display.set_mode(dimensions)
        self.gui_board = GUIBoard(
            *self.difficulty.get_shape(),
            offset_x=0,
            offset_y=0,
        )
        running = True

        while running:
            self.screen.fill((255, 255, 255))
            pygame.display.flip()


if __name__ == '__main__':
    gui = GUI()
    gui.run_main_menu()
