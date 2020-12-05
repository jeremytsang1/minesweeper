import pygame
from minesweeper.ui.gui.main_menu import MainMenu
from minesweeper.ui.gui.difficulty import Difficulty
from minesweeper.game.game import Game


class GUI():
    def __init__(self):
        pygame.init()
        self.difficulty = Difficulty()
        self.game = None
        self.gui_board = None
        self.main_menu = MainMenu(self.set_difficulty, self.run_game)

    def set_difficulty(self, description, level):
        self.difficulty.set_difficulty(level)
        print(self.difficulty)

    def run_main_menu(self):
        self.main_menu.show_menu()

    def run_game(self):
        raise NotImplementedError


if __name__ == '__main__':
    gui = GUI()
    gui.run_main_menu()
