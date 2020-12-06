import pygame
import pygame_menu
from minesweeper.ui.gui.main_menu import MainMenu
from minesweeper.ui.gui.custom_level_menu import CustomLevelMenu
from minesweeper.ui.gui.difficulty import Difficulty
from minesweeper.ui.gui.gui_board import GUIBoard
from minesweeper.game.game import Game


class GUI():
    # Mouse event buttons
    MOUSE_LEFT = 1
    MOUSE_MIDDLE = 2
    MOUSE_RIGHT = 3

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
        self.preset = True  # Starts off as EASY which is one of the presets.
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
        self.add_sprites(self.gui_board.get_sprites())

        self.main_game_loop()

    def main_game_loop(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.process_click(event)
                if event.type == pygame.QUIT:  # Go back to main menu
                    self.end_game()
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Go back to main menu
                        self.end_game()
                        running = False

            self.screen.fill((255, 255, 255))

            # Draw all the sprites
            self.all_sprites.draw(self.screen)

            for sprite in self.gui_board.get_sprites():
                sprite.draw(self.screen)

            pygame.display.flip()

    def process_click(self, event):
        for gui_cell in self.gui_board.get_sprites():
            if gui_cell.is_mouse_up(event.pos):
                self.process_mouse_button(event.button, gui_cell)
                break  # don't bother searching other cells if found click

    def process_mouse_button(self, button, gui_cell):
        row_col_pos = gui_cell.get_row_col_pos()
        if button == self.MOUSE_LEFT:
            print(f"{row_col_pos}: attempting to open")
            if self.game is None:
                self.create_game(gui_cell)

            self.open_cell(gui_cell)
        elif button == self.MOUSE_RIGHT:
            print(f"{row_col_pos}: attempting to toggle flag")
            self.toggle_flag(gui_cell)
        elif button == self.MOUSE_MIDDLE:
            print(f"{row_col_pos}: attempting to chord")
            self.chord_cell(gui_cell)
        else:
            print('Irrelevant mouse click')

    def open_cell(self, gui_cell):
        pass

    def toggle_flag(self, gui_cell):
        if self.game is None:
            print("No flagging on the first turn!")  # TODO
        else:
            raise Exception("TODO")

    def chord_cell(self, gui_cell):
        if self.game is None:
            print("No number cells to chord yet!")  # TODO
        else:
            raise Exception("TODO")

    def create_game(self, gui_cell):
        self.game = Game(
            *self.difficulty.get_shape(),
            self.difficulty.get_bomb_count(),
            *gui_cell.get_row_col_pos()
        )

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
        self.game = None
        self.gui_board.kill_gui_board()
        self.gui_board = None
        self.preset = True  # Starts off as EASY which is one of the presets.
        self.run_main_menu()


if __name__ == '__main__':
    gui = GUI()
    gui.run_main_menu()
