import pygame
import pygame_menu
from minesweeper.ui.gui.main_menu import MainMenu
from minesweeper.ui.gui.custom_level_menu import CustomLevelMenu
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
        self.theme = self.create_theme()
        self.main_menu = MainMenu(self.set_difficulty, self.press_play_button, self.theme)
        self.custom_level_menu = None
        self.preset = None
        self.all_sprites = pygame.sprite.Group()

    @staticmethod
    def create_theme():
        theme = pygame_menu.themes.THEME_SOLARIZED
        theme.menubar_close_button = False
        return theme

    def set_difficulty(self, description, level):
        self.preset = self.difficulty.set_difficulty(level)

    def run_main_menu(self):
        self.screen = pygame.display.set_mode((MainMenu.WIDTH,
                                               MainMenu.HEIGHT))
        self.main_menu.show_menu(self.screen)

    def press_play_button(self):
        if not self.preset:
            self.ask_user_for_custom_settings()
        else:
            self.run_game()

    def run_game(self):
        self.game = None

        dimensions = GUIBoard.compute_dimensions(*self.difficulty.get_shape())
        self.screen = pygame.display.set_mode(dimensions)
        self.gui_board = GUIBoard(
            *self.difficulty.get_shape(),
            offset_x=0,
            offset_y=0,
        )
        self.add_sprites(self.gui_board.get_gui_cells())

        self.main_game_loop()

    def main_game_loop(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    print(pygame.mouse.get_pressed())
                if event.type == pygame.QUIT:  # Go back to main menu
                    self.end_game()
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Go back to main menu
                        self.end_game()
                        running = False

            self.screen.fill((255, 255, 255))
            pygame.display.flip()

    def add_sprites(self, sprites):
        for sprite in sprites:
            self.all_sprites.add(sprite)

    def ask_user_for_custom_settings(self):
        self.custom_level_menu = CustomLevelMenu(
            self.difficulty,
            self.run_game,
            self.theme,
            self.screen
        )
        self.custom_level_menu.show_menu()
        del self.custom_level_menu
        self.custom_level_menu = None
    
    def end_game(self):
        self.gui_board.kill_gui_board()
        self.gui_board = None
        self.preset = None
        self.run_main_menu()


if __name__ == '__main__':
    gui = GUI()
    gui.run_main_menu()
